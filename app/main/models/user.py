
from app.main.extensions import db
import enum
from datetime import datetime, timezone


class UserRole(enum.Enum):
    tenant = "tenant"
    landlord = "landlord"



class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"schema":"rms"}

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False, index = True)
    phone = db.Column(db.String(20), unique = True, nullable = False, index = True)
    
    password_hash = db.Column(db.String(128), nullable = False)

    identity_verified = db.Column(db.Boolean, default = False)
    profile_image = db.Column(db.String, nullable = True)
    is_active = db.Column(db.Boolean, default = True)

    role = db.Column(db.Enum(UserRole), default = UserRole.tenant, nullable = False)

    created_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc))


    # why lamda?
    # Using a lambda ensures the datetime is evaluated at runtime, not at the time the class is defined.