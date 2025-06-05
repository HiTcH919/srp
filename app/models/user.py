from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin): # Inherit from UserMixin
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True) # Nullable if password not set yet, or for external auth
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to ServiceOrder
    # Ensure 'ServiceOrder' is imported or will be when SQLAlchemy resolves relationships.
    # The foreign_keys parameter is crucial if there are multiple FKs to User table from ServiceOrder.
    # If ServiceOrder.created_by_user_id is the only FK to User, it might not be needed.
    service_orders_authored = db.relationship('ServiceOrder', backref='author', lazy='dynamic', foreign_keys='ServiceOrder.created_by_user_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
