from app import db

class SecurityForceGroup(db.Model):
    __tablename__ = 'security_force_groups'
    id = db.Column(db.Integer, primary_key=True)
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False)
    force_type = db.Column(db.String(50), nullable=True) # 'central', 'security_forces'
    group_leader_type = db.Column(db.String(50), nullable=True) # 'officer', 'individual'
    group_leader_rank = db.Column(db.String(100), nullable=True)
    group_leader_name = db.Column(db.String(150), nullable=True)
    group_leader_phone = db.Column(db.String(50), nullable=True)
    group_count = db.Column(db.Integer, nullable=True)
    vehicle_type = db.Column(db.String(100), nullable=True) # Vehicle assigned to group
    vehicle_number = db.Column(db.String(50), nullable=True)
    vehicle_driver_rank = db.Column(db.String(100), nullable=True)
    vehicle_driver_name = db.Column(db.String(150), nullable=True)
    vehicle_driver_phone = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<SecurityForceGroup {self.id} for SO {self.service_order_id}>'
