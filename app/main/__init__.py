# Flask App Factory

from flask import Flask 
from app.main.config import Config
from app.main.extensions import db, ma, jwt, bcrypt, mail, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # binding the extensions to app instance here,
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    

    # TODO: Register blueprints here

    # from app.main.routes.user_routes import user_bp # type: ignore
    from app.main.controllers.auth_controller import auth_bp 
    from app.main.controllers.property_image_routes import property_image_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(property_image_bp, url_prefix="/api/images")
    
    

    return app
    

    