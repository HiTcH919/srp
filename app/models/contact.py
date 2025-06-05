# Contact model for the phonebook will go here.
# Example using Flask-SQLAlchemy:
# from app.models import db # Assuming db is initialized in models/__init__.py

# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     phone_number = db.Column(db.String(20))
#     email = db.Column(db.String(120))
#     address = db.Column(db.String(200))
#     notes = db.Column(db.Text)

#     def __repr__(self):
#         return f'<Contact {self.name}>'

class Contact: # Placeholder
    def __init__(self, id, name, phone_number):
        self.id = id
        self.name = name
        self.phone_number = phone_number

    def __repr__(self):
        return f'<Contact {self.name}>'
