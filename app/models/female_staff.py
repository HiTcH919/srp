from app import db

class FemaleStaffMember(db.Model):
    __tablename__ = 'female_staff_members'
    id = db.Column(db.Integer, primary_key=True)
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False)
    is_officer_in_charge = db.Column(db.Boolean, default=False)
    rank = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    specialization = db.Column(db.String(100), nullable=True) # Only for officer_in_charge

    def __repr__(self):
        return f'<FemaleStaffMember {self.name} for SO {self.service_order_id}>'
