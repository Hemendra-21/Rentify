
from app.main.extensions import db

user_roles = db.Table(
    'user_roles',
    db.metadata,                 
    db.Column('user_id', db.Integer, db.ForeignKey('rms.users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('rms.roles.id'), primary_key=True),
    schema='rms'
)
