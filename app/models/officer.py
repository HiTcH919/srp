from app import db

class Officer(db.Model):
    __tablename__ = 'officers'
    id = db.Column(db.Integer, primary_key=True)
    # Corrected ForeignKey to 'service_orders.id' assuming ServiceOrder.__tablename__ = 'service_orders'
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False)
    officer_type = db.Column(db.String(100)) # e.g., 'general_supervisor', 'system_supervisor', 'detective_supervisor'
    rank = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Officer {self.name} ({self.officer_type}) for SO {self.service_order_id}>'
