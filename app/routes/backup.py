# Backup and restore routes will go here.
from flask import Blueprint, render_template, current_app, send_file, request, flash, redirect, url_for
import os
import subprocess
# from flask_login import login_required

backup_bp = Blueprint('backup', __name__)

# @backup_bp.route('/backup/create')
# @login_required
# def create_backup():
#     # Logic to create a database backup
#     # Example: using subprocess to call pg_dump or sqlite3 .dump
#     # db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
#     # backup_file = 'backup.db.sql' # Name it appropriately
#     # try:
#     #     subprocess.run(['sqlite3', db_path, f'.dump > {backup_file}'], check=True, shell=True)
#     #     flash(f'Backup created successfully: {backup_file}', 'success')
#     #     return send_file(backup_file, as_attachment=True)
#     # except Exception as e:
#     #     flash(f'Error creating backup: {e}', 'danger')
#     #     return redirect(url_for('dashboard.index')) # Or some other appropriate page
#     return "Create backup endpoint"

# @backup_bp.route('/backup/restore', methods=['POST'])
# @login_required
# def restore_backup():
#     # Logic to restore database from a backup file
#     # Ensure to handle file uploads securely
#     # if 'backup_file' not in request.files:
#     #     flash('No backup file part', 'warning')
#     #     return redirect(request.url)
#     # file = request.files['backup_file']
#     # if file.filename == '':
#     #     flash('No selected backup file', 'warning')
#     #     return redirect(request.url)
#     # if file:
#     #     # filename = secure_filename(file.filename) # Make sure to import secure_filename
#     #     # file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename) # Define UPLOAD_FOLDER
#     #     # file.save(file_path)
#     #     # db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
#     #     # try:
#     #     #     # Stop the app, restore, restart, or ensure no connections during restore
#     #     #     subprocess.run(['sqlite3', db_path, f'< {file_path}'], check=True, shell=True)
#     #     #     flash('Backup restored successfully!', 'success')
#     #     # except Exception as e:
#     #     #     flash(f'Error restoring backup: {e}', 'danger')
#     #     # return redirect(url_for('dashboard.index'))
#     return "Restore backup endpoint"

@backup_bp.route('/backup')
# @login_required
def backup_page():
    return render_template('backup.html') # Need to create this template
