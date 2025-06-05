from app import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False)
    vehicle_category = db.Column(db.String(100)) # 'emergency_car', 'other_vehicle'

    # Fields for Emergency Car
    chief_type = db.Column(db.String(50), nullable=True) # 'officer', 'individual'
    chief_rank = db.Column(db.String(100), nullable=True)
    chief_name = db.Column(db.String(150), nullable=True)
    chief_phone = db.Column(db.String(50), nullable=True)

    # Fields for Both / Other
    vehicle_number = db.Column(db.String(50), nullable=True)
    vehicle_type = db.Column(db.String(100), nullable=True) # Specific type like 'Lorry', 'Sedan'
    driver_rank = db.Column(db.String(100), nullable=True)
    driver_name = db.Column(db.String(150), nullable=True)
    driver_phone = db.Column(db.String(50), nullable=True)
    driver_license_number = db.Column(db.String(50), nullable=True) # For emergency car driver

    # Fields for Other Vehicle
    capacity_load = db.Column(db.String(100), nullable=True)
    purpose = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Vehicle {self.vehicle_number} ({self.vehicle_category}) for SO {self.service_order_id}>'
