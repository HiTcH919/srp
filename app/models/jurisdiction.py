from app import db

class JurisdictionInfo(db.Model):
    __tablename__ = 'jurisdiction_info'
    id = db.Column(db.Integer, primary_key=True)
    # Corrected ForeignKey to 'service_orders.id'
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False, unique=True)
    accompanying_entity = db.Column(db.String(200), nullable=True)
    responsible_person_title = db.Column(db.String(100), nullable=True)
    responsible_person_name = db.Column(db.String(150), nullable=True)
    responsible_person_phone = db.Column(db.String(50), nullable=True)
    responsible_person_email = db.Column(db.String(120), nullable=True)
    special_notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<JurisdictionInfo for SO {self.service_order_id}>'
