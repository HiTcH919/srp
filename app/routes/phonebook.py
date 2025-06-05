# Phonebook routes will go here.
from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.contact import Contact # Assuming a Contact model
# from app import db # Assuming a db object from Flask-SQLAlchemy
# from flask_login import login_required

phonebook_bp = Blueprint('phonebook', __name__)

@phonebook_bp.route('/phonebook')
# @login_required
def list_contacts():
    # contacts = Contact.query.all()
    # return render_template('phonebook.html', contacts=contacts)
    return render_template('phonebook.html')

@phonebook_bp.route('/phonebook/new', methods=['GET', 'POST'])
# @login_required
def new_contact():
    # if request.method == 'POST':
    #     # Process form data and create new contact
    #     flash('Contact added successfully!')
    #     return redirect(url_for('phonebook.list_contacts'))
    # return render_template('new_contact.html')
    return "Form for new contact"

@phonebook_bp.route('/phonebook/edit/<int:contact_id>', methods=['GET', 'POST'])
# @login_required
def edit_contact(contact_id):
    # contact = Contact.query.get_or_404(contact_id)
    # if request.method == 'POST':
    #     # Process form data and update contact
    #     flash('Contact updated successfully!')
    #     return redirect(url_for('phonebook.list_contacts'))
    # return render_template('edit_contact.html', contact=contact)
    return f"Editing contact {contact_id}"

@phonebook_bp.route('/phonebook/delete/<int:contact_id>', methods=['POST']) # Should be POST for deletion
# @login_required
def delete_contact(contact_id):
    # contact = Contact.query.get_or_404(contact_id)
    # db.session.delete(contact)
    # db.session.commit()
    # flash('Contact deleted successfully!')
    # return redirect(url_for('phonebook.list_contacts'))
    return f"Deleting contact {contact_id}"
