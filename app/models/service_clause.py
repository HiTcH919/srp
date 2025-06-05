from app import db

class ServiceOrderClause(db.Model):
    __tablename__ = 'service_order_clauses'
    id = db.Column(db.Integer, primary_key=True)
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False)
    clause_type = db.Column(db.String(50), nullable=True) # 'dispatch', 'delivery', 'return'
    clause_number = db.Column(db.String(100), nullable=True)
    clause_document = db.Column(db.String(200), nullable=True)
    additional_details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ServiceOrderClause {self.clause_type} for SO {self.service_order_id}>'
