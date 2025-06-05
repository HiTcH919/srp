from app import db

class DeporteeAccused(db.Model):
    __tablename__ = 'deportees_accused'
    id = db.Column(db.Integer, primary_key=True)
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False)
    name = db.Column(db.String(150), nullable=True)
    case_number = db.Column(db.String(100), nullable=True)
    national_id = db.Column(db.String(50), nullable=True)
    charge = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<DeporteeAccused {self.name} for SO {self.service_order_id}>'
