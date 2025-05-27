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

    from app.main.routes.user_routes import user_bp # type: ignore
    from app.main.routes.auth_routes import auth_bp # type: ignore

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    
    

    return app
    

    