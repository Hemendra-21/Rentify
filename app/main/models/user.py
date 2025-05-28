
from app.main.extensions import db, bcrypt
from datetime import datetime, timezone

from app.main.models.role import Role
from app.main.models.user_roles import user_roles


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

    roles = db.relationship('Role', secondary=user_roles, back_populates="users")
    created_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc))


    # why lamda?
    # Using a lambda ensures the datetime is evaluated at runtime, not at the time the class is defined.

    def set_password(self, raw_password: str):
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password: str):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    

    def add_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if role and role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        if role and role in self.roles:
            self.roles.remove(role)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)