from app.main.extensions import db 
from .user_roles import user_roles

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {"schema":"rms"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', secondary=user_roles, back_populates="roles")

    def __repr__(self):
        return f"<Role {self.name}>"