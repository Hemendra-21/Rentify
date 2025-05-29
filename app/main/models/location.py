from sqlalchemy import func
from app.main.extensions import db

class Location(db.Model):
    __tablename__ = 'locations'
    __table_args__ = {"schema":"rms"}

    id = db.Column(db.Integer, primary_key=True)
    # property_id = db.Column(db.Integer, db.ForeignKey('rms.properties.id'), nullable=False, unique=True)

    street = db.Column(db.String(255), nullable=False)
    locality = db.Column(db.String(100), nullable=False)
    near_by = db.Column(db.String(255))
    
    city = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # property = db.relationship("Property", back_populates="locations")
