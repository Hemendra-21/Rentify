from app.main import create_app
from app.main.extensions import db 
from app.main.models.user import User


app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully")