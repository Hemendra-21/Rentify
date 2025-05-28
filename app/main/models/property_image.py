from app.main.extensions import db
from sqlalchemy.sql import func

class PropertyImage(db.Model):
    __tablename__ = 'property_images'
    __table_args__ = {"schema":"rms"}

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('rms.properties.id'), nullable=False)
    image_url = db.Column(db.String(512), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    property = db.relationship("Property", back_populates="images")
