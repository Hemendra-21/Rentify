from flask import Blueprint, request, jsonify
from app.main.schema.user_schema import UserRegisterSchema
from app.main.services.auth_service import AuthService 
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.main.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

register_schema = UserRegisterSchema()

@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        user_data = register_schema.load(request.get_json())
        return AuthService.register_user(user_data)
        # return jsonify(result), 201
    
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500



@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        return AuthService.login_user(data)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occured: {str(e)}"}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        return AuthService.forgot_password(request.json)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occured: {str(e)}"}), 500



@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        return AuthService.reset_password(request.json)
    except Exception as e:
        return jsonify({"error": f"An unexpected error occured: {str(e)}"}), 500



@auth_bp.route('/current-user', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    return AuthService.get_current_user(user_id)