from datetime import datetime, timezone
from app.main.extensions import db

class Property(db.Model):
    __tablename__ = 'properties'
    __table_args__ = {"schema":"rms"}

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('rms.users.id'), nullable=False)
    property_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    property_type = db.Column(db.String(50), nullable=False)  # Apartment, Villa, etc.
    bhk_type = db.Column(db.String(10), nullable=False)        # 1 BHK, 2 BHK, etc.
    bathrooms = db.Column(db.Integer, nullable=False)
    area_sqft = db.Column(db.Float, nullable=False)
    rent_price = db.Column(db.Float, nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="available")     # available, rented, etc.
    location_id = db.Column(db.Integer, db.ForeignKey('rms.locations.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = db.relationship('User', backref='properties')
    location = db.relationship('Location', backref='properties')
    images = db.relationship('PropertyImage', backref='property', cascade='all, delete-orphan')
