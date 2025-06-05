from app import db
from datetime import datetime, timezone, date, time

# It's good practice to import related models for clarity, even if SQLAlchemy can resolve strings.
# However, to avoid circular imports if these models also import ServiceOrder,
# using strings for relationship definitions is safer and standard.
# from .officer import Officer # Example
# from .security_force_group import SecurityForceGroup # Example

class ServiceOrder(db.Model):
    __tablename__ = 'service_orders'

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(200), nullable=False)

    service_date_on = db.Column(db.Date, nullable=True)
    service_time_at = db.Column(db.Time, nullable=True)

    sector = db.Column(db.String(100), nullable=True)
    police_station_department = db.Column(db.String(150), nullable=True)
    general_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Draft')

    # Security level for deportees/accused associated with this service order
    security_level = db.Column(db.String(50), nullable=True) # e.g., 'Normal', 'Medium', 'High'

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 'author' backref is on User.service_orders_authored

    # Relationships to detail models
    # Cascade "all, delete-orphan" means related objects are deleted when the ServiceOrder is deleted.
    officers = db.relationship('Officer', backref='service_order', lazy='dynamic', cascade="all, delete-orphan")
    security_force_groups = db.relationship('SecurityForceGroup', backref='service_order', lazy='dynamic', cascade="all, delete-orphan")
    female_staff_members = db.relationship('FemaleStaffMember', backref='service_order', lazy='dynamic', cascade="all, delete-orphan")
    vehicles = db.relationship('Vehicle', backref='service_order', lazy='dynamic', cascade="all, delete-orphan")
    service_clauses = db.relationship('ServiceOrderClause', backref='service_order', lazy='dynamic', cascade="all, delete-orphan")
    jurisdiction_info = db.relationship('JurisdictionInfo', backref='service_order', uselist=False, cascade="all, delete-orphan") # One-to-one
    deportees_accused = db.relationship('DeporteeAccused', backref='service_order', lazy='dynamic', cascade="all, delete-orphan")
    documents = db.relationship('Document', backref='service_order', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<ServiceOrder {self.id}: {self.service_name}>'
