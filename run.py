import unittest
from flask_migrate import Migrate

from app.main import create_app
from app.main.extensions import db
from app.main.seed import seed_roles

app = create_app()
migrate = Migrate(app, db)


if __name__ == "__main__":
    with app.app_context():
        seed_roles()
    app.run(debug=True)