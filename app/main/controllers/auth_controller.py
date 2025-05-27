from flask import Blueprint, request, jsonify
from app.main.schema.user_schema import UserRegisterSchema
from app.main.services.auth_service import AuthService 
from marshmallow import ValidationError

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