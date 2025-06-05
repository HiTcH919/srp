from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort, send_from_directory
from flask_login import login_required, current_user
from app import db
from app.models.service_order import ServiceOrder
from app.models.officer import Officer
from app.models.security_force_group import SecurityForceGroup
from app.models.female_staff import FemaleStaffMember
from app.models.vehicle import Vehicle
from app.models.service_clause import ServiceOrderClause
from app.models.jurisdiction import JurisdictionInfo
from app.models.deportee_accused import DeporteeAccused
from app.models.document import Document
from datetime import datetime as dt_parser, date, time
import json
import os
import uuid
from werkzeug.utils import secure_filename

service_orders_bp = Blueprint('service_orders', __name__, url_prefix='/service')

@service_orders_bp.route('/')
@login_required
def list_orders():
    return "قائمة أوامر الخدمة (سيتم التنفيذ لاحقاً)"

@service_orders_bp.route('/new/basic-info', methods=['GET', 'POST'])
@login_required
def new_service_basic_info():
    return render_template('new_service_basic_info.html')

@service_orders_bp.route('/new/human-resources', methods=['GET', 'POST'])
@login_required
def new_service_human_resources():
    return render_template('new_service_human_resources.html')

@service_orders_bp.route('/new/vehicles', methods=['GET', 'POST'])
@login_required
def new_service_vehicles():
    return render_template('new_service_vehicles.html')

@service_orders_bp.route('/new/terms', methods=['GET', 'POST'])
@login_required
def new_service_terms():
    return render_template('new_service_terms.html')

@service_orders_bp.route('/new/review-docs', methods=['GET'])
@login_required
def new_service_review_docs():
    return render_template('new_service_review.html')


@service_orders_bp.route('/submit', methods=['POST'])
@login_required
def submit_service_order():
    if request.method == 'POST':
        try:
            # Basic Information
            service_name = request.form.get('basic_info_service_name')
            service_date_str = request.form.get('basic_info_service_date_on')
            service_time_str = request.form.get('basic_info_service_time_at')
            sector = request.form.get('basic_info_sector')
            police_station_department = request.form.get('basic_info_police_station_department')
            general_notes = request.form.get('basic_info_general_notes')
            security_level = request.form.get('terms_security_level')

            if not all([service_name, service_date_str, service_time_str]):
                flash('اسم الخدمة وتاريخها ووقتها حقول مطلوبة من المعلومات الأساسية.', 'danger')
                return redirect(url_for('service_orders.new_service_review_docs'))

            parsed_date = None
            if service_date_str:
                try:
                    parsed_date = dt_parser.strptime(service_date_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('صيغة التاريخ غير صحيحة. الرجاء استخدام YYYY-MM-DD.', 'danger')
                    return redirect(url_for('service_orders.new_service_review_docs'))

            parsed_time = None
            if service_time_str:
                try:
                    parsed_time = dt_parser.strptime(service_time_str, '%H:%M').time()
                except ValueError:
                    flash('صيغة الوقت غير صحيحة. الرجاء استخدام HH:MM.', 'danger')
                    return redirect(url_for('service_orders.new_service_review_docs'))

            new_service_order = ServiceOrder(
                service_name=service_name, service_date_on=parsed_date, service_time_at=parsed_time,
                sector=sector, police_station_department=police_station_department,
                general_notes=general_notes, user_id=current_user.id, status='Submitted',
                security_level=security_level
            )
            db.session.add(new_service_order)

            # Human Resources Data
            officer_types_map = {'gs': 'مشرف عام الخدمة', 'ss': 'مشرف النظام', 'ds': 'مشرف المباحث'}
            for prefix, type_desc in officer_types_map.items():
                name = request.form.get(f'human_resources_{prefix}_name')
                if name:
                    officer = Officer(officer_type=type_desc, rank=request.form.get(f'human_resources_{prefix}_rank'),
                                      name=name, phone=request.form.get(f'human_resources_{prefix}_phone'),
                                      unit=request.form.get(f'human_resources_{prefix}_unit'))
                    new_service_order.officers.append(officer)

            sf_groups_json = request.form.get('human_resources_security_force_groups_json')
            if sf_groups_json:
                try:
                    sf_groups_data = json.loads(sf_groups_json)
                    for item in sf_groups_data:
                        sf_group = SecurityForceGroup(
                            force_type=item.get('force_type'), group_leader_type=item.get('group_leader_type'),
                            group_leader_rank=item.get('group_leader_rank'), group_leader_name=item.get('group_leader_name'),
                            group_leader_phone=item.get('group_leader_phone'),
                            group_count=int(item.get('group_count', 0)) if item.get('group_count') else None,
                            vehicle_type=item.get('vehicle_type'), vehicle_number=item.get('vehicle_number'),
                            vehicle_driver_rank=item.get('vehicle_driver_rank'), vehicle_driver_name=item.get('vehicle_driver_name'),
                            vehicle_driver_phone=item.get('vehicle_driver_phone'))
                        new_service_order.security_force_groups.append(sf_group)
                except (json.JSONDecodeError, ValueError) as e: flash(f'خطأ في معالجة بيانات قوات الأمن: {e}', 'danger')

            fs_oic_name = request.form.get('human_resources_foic_name')
            if fs_oic_name:
                 fs_oic = FemaleStaffMember(is_officer_in_charge=True, rank=request.form.get('human_resources_foic_rank'),
                                           name=fs_oic_name, phone=request.form.get('human_resources_foic_phone'),
                                           specialization=request.form.get('human_resources_foic_specialization'))
                 new_service_order.female_staff_members.append(fs_oic)

            fs_names = request.form.getlist('human_resources_fs_name[]')
            fs_ranks = request.form.getlist('human_resources_fs_rank[]')
            fs_phones = request.form.getlist('human_resources_fs_phone[]')
            for i in range(len(fs_names)):
                if fs_names[i]:
                    fs_member = FemaleStaffMember(is_officer_in_charge=False, rank=fs_ranks[i] if i < len(fs_ranks) else None,
                                                name=fs_names[i], phone=fs_phones[i] if i < len(fs_phones) else None)
                    new_service_order.female_staff_members.append(fs_member)

            # Vehicles Data
            ec_vehicle_number = request.form.get('vehicles_ec_car_number')
            if ec_vehicle_number:
                emergency_car = Vehicle(
                    vehicle_category='emergency_car', chief_type=request.form.get('vehicles_ec_chief_type'),
                    chief_rank=request.form.get('vehicles_ec_chief_rank'), chief_name=request.form.get('vehicles_ec_chief_name'),
                    chief_phone=request.form.get('vehicles_ec_chief_phone'), vehicle_number=ec_vehicle_number,
                    vehicle_type=request.form.get('vehicles_ec_car_type'), driver_rank=request.form.get('vehicles_ec_driver_rank'),
                    driver_name=request.form.get('vehicles_ec_driver_name'), driver_phone=request.form.get('vehicles_ec_driver_phone'),
                    driver_license_number=request.form.get('vehicles_ec_driver_license'))
                new_service_order.vehicles.append(emergency_car)

            other_vehicles_json = request.form.get('vehicles_other_vehicles_list_json')
            if other_vehicles_json:
                try:
                    other_vehicles_data = json.loads(other_vehicles_json)
                    for item in other_vehicles_data:
                        vehicle = Vehicle(
                            vehicle_category='other_vehicle', vehicle_type=item.get('type'),
                            vehicle_number=item.get('number'), driver_rank=item.get('driver_rank'),
                            driver_name=item.get('driver_name'), driver_phone=item.get('driver_phone'),
                            capacity_load=item.get('capacity_load'), purpose=item.get('purpose'))
                        new_service_order.vehicles.append(vehicle)
                except (json.JSONDecodeError, ValueError) as e: flash(f'خطأ في معالجة بيانات المركبات الأخرى: {e}', 'danger')

            # Service Terms and Details Data
            clause_types_fields = {
                'dispatch': ('terms_dispatch_clause_number', 'terms_dispatch_clause_document'),
                'delivery': ('terms_delivery_clause_number', 'terms_delivery_clause_document'),
                'return': ('terms_return_clause_number', 'terms_return_clause_document'),}
            common_additional_details = request.form.get('terms_clauses_additional_details')
            clauses_added_details = False
            for clause_type_key, (num_field, doc_field) in clause_types_fields.items():
                clause_number = request.form.get(num_field)
                clause_document = request.form.get(doc_field)
                if clause_number or clause_document:
                    current_details = None
                    if common_additional_details and not clauses_added_details:
                        current_details = common_additional_details
                        clauses_added_details = True
                    new_clause = ServiceOrderClause(clause_type=clause_type_key, clause_number=clause_number,
                                                    clause_document=clause_document, additional_details=current_details)
                    new_service_order.service_clauses.append(new_clause)
            if not clauses_added_details and common_additional_details:
                generic_clause = ServiceOrderClause(clause_type='general_details', additional_details=common_additional_details)
                new_service_order.service_clauses.append(generic_clause)

            ji_responsible_name = request.form.get('terms_ji_responsible_person_name')
            if ji_responsible_name:
                new_jurisdiction_info = JurisdictionInfo(
                    accompanying_entity=request.form.get('terms_ji_accompanying_entity'),
                    responsible_person_title=request.form.get('terms_ji_responsible_person_title'),
                    responsible_person_name=ji_responsible_name,
                    responsible_person_phone=request.form.get('terms_ji_responsible_person_phone'),
                    responsible_person_email=request.form.get('terms_ji_responsible_person_email'),
                    special_notes=request.form.get('terms_ji_special_notes'))
                new_service_order.jurisdiction_info = new_jurisdiction_info

            deportees_json = request.form.get('terms_deportees_accused_list_json')
            if deportees_json:
                try:
                    deportees_data = json.loads(deportees_json)
                    for item in deportees_data:
                        deportee = DeporteeAccused(name=item.get('name'), case_number=item.get('case_number'),
                                                  national_id=item.get('national_id'), charge=item.get('charge'))
                        new_service_order.deportees_accused.append(deportee)
                except (json.JSONDecodeError, ValueError) as e: flash(f'خطأ في معالجة بيانات المرحلين/المتهمين: {e}', 'danger')

            # --- File Uploads and Documents ---
            upload_folder = current_app.config['UPLOAD_FOLDER']

            image_file = request.files.get('service_order_image_file')
            if image_file and image_file.filename:
                original_filename = secure_filename(image_file.filename)
                file_ext = os.path.splitext(original_filename)[1]
                unique_filename = str(uuid.uuid4()) + file_ext
                image_file.save(os.path.join(upload_folder, unique_filename))
                doc = Document(file_name=original_filename, file_path=unique_filename, document_type='service_order_image')
                new_service_order.documents.append(doc)

            additional_files = request.files.getlist('additional_document_files')
            for file in additional_files:
                if file and file.filename:
                    original_filename = secure_filename(file.filename)
                    file_ext = os.path.splitext(original_filename)[1]
                    unique_filename = str(uuid.uuid4()) + file_ext
                    file.save(os.path.join(upload_folder, unique_filename))
                    doc = Document(file_name=original_filename, file_path=unique_filename, document_type='additional_document')
                    new_service_order.documents.append(doc)

            db.session.commit()
            flash(f"أمر خدمة '{service_name}' وجميع تفاصيله بما في ذلك المستندات تم حفظها بنجاح!", "success")
            return redirect(url_for('dashboard.home'))

        except Exception as e:
            db.session.rollback()
            flash(f"حدث خطأ أثناء تقديم أمر الخدمة: {str(e)}", "danger")
            print(f"Error submitting service order: {e}")
            return redirect(url_for('service_orders.new_service_review_docs'))

    return redirect(url_for('service_orders.new_service_review_docs'))


@service_orders_bp.route('/<int:order_id>')
@login_required
def view_order(order_id):
    order = ServiceOrder.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    title = f"تفاصيل الخدمة: {order.service_name}"
    return render_template('service_order_detail.html', service_order=order, title=title)

@service_orders_bp.route('/<int:order_id>/edit_basic', methods=['GET'])
@login_required
def edit_service_order_basic_form(order_id):
    service_order = ServiceOrder.query.get_or_404(order_id)

    if not current_user.is_admin and service_order.user_id != current_user.id:
        abort(403) # Forbidden

    form_data = {
        'service_name': service_order.service_name,
        'service_date_on': service_order.service_date_on.isoformat() if service_order.service_date_on else '',
        'service_time_at': service_order.service_time_at.strftime('%H:%M') if service_order.service_time_at else '',
        'sector': service_order.sector,
        'police_station_department': service_order.police_station_department,
        'general_notes': service_order.general_notes
        # Security level is typically part of the 'terms' step, so not included here for 'basic_info' edit.
    }

    return render_template(
        'new_service_basic_info.html', # Re-use the same template
        edit_mode=True,
        service_order_id=service_order.id,
        form_data=form_data,
        title=f"تعديل البيانات الأساسية لـ: {service_order.service_name}"
    )

@service_orders_bp.route('/<int:order_id>/edit_basic/submit', methods=['POST']) # Corrected action name from template
@login_required
def submit_edit_service_order_basic(order_id):
    service_order = ServiceOrder.query.get_or_404(order_id)

    if not current_user.is_admin and service_order.user_id != current_user.id:
        abort(403) # Forbidden

    if request.method == 'POST':
        try:
            # Retrieve updated data from form
            service_order.service_name = request.form.get('service_name')
            service_date_str = request.form.get('service_date_on')
            service_time_str = request.form.get('service_time_at')
            service_order.sector = request.form.get('sector')
            service_order.police_station_department = request.form.get('police_station_department')
            service_order.general_notes = request.form.get('general_notes')
            # Security level is not edited in this specific form for basic info

            # Validate required fields
            if not all([service_order.service_name, service_date_str, service_time_str]):
                flash('اسم الخدمة والتاريخ والوقت حقول إلزامية.', 'danger')
                # To repopulate form correctly, pass back current (potentially invalid) form data
                # or re-query original and merge with request.form
                return redirect(url_for('service_orders.edit_service_order_basic_form', order_id=order_id))

            # Parse date and time strings
            if service_date_str:
                try:
                    service_order.service_date_on = dt_parser.strptime(service_date_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('صيغة تاريخ الخدمة غير صحيحة. استخدم YYYY-MM-DD.', 'danger')
                    return redirect(url_for('service_orders.edit_service_order_basic_form', order_id=order_id))
            else:
                service_order.service_date_on = None # Allow clearing the date

            if service_time_str:
                try:
                    service_order.service_time_at = dt_parser.strptime(service_time_str, '%H:%M').time()
                except ValueError:
                    flash('صيغة وقت الخدمة غير صحيحة. استخدم HH:MM.', 'danger')
                    return redirect(url_for('service_orders.edit_service_order_basic_form', order_id=order_id))
            else:
                service_order.service_time_at = None # Allow clearing the time

            # updated_at is handled by onupdate in the model, but explicit is fine too.
            # from datetime import timezone # Make sure timezone is imported if using this
            # service_order.updated_at = dt_parser.now(timezone.utc)

            db.session.commit()
            flash(f"المعلومات الأساسية لأمر الخدمة '{service_order.service_name}' تم تحديثها بنجاح!", "success")
            return redirect(url_for('service_orders.view_service_order', order_id=service_order.id))

        except Exception as e:
            db.session.rollback()
            flash(f"حدث خطأ أثناء تحديث المعلومات الأساسية: {str(e)}", "danger")
            print(f"Error updating basic info for SO {order_id}: {e}")
            return redirect(url_for('service_orders.edit_service_order_basic_form', order_id=order_id))

    # Fallback for GET request to this URL
    return redirect(url_for('service_orders.edit_service_order_basic_form', order_id=order_id))

@service_orders_bp.route('/download_document/<int:document_id>')
@login_required
def download_document(document_id):
    doc = Document.query.get_or_404(document_id)

    if doc.service_order.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    upload_folder = current_app.config['UPLOAD_FOLDER']
    try:
        return send_from_directory(
            upload_folder,
            doc.file_path,
            as_attachment=True,
            download_name=doc.file_name
        )
    except FileNotFoundError:
        abort(404, "File not found on server.")
