from flask import Blueprint
from app.main.controllers.auth_controller import auth_bp # type: ignore



# Route to controller
# auth_bp.route('/login', methods=['POST'])(login_user)