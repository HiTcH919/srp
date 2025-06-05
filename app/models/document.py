from app import db
from datetime import datetime, timezone # Corrected import

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    service_order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    document_type = db.Column(db.String(100), nullable=True) # 'service_order_image', 'additional_document'
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Document {self.file_name} for SO {self.service_order_id}>'
