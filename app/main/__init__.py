# Flask App Factory

from flask import Flask 
from app.main.config import Config
from app.main.extensions import db, ma, jwt, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # binding the extensions to app instance here,
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # TODO: Register blueprints here

    return app
    

    