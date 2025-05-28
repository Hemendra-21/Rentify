from app.main.extensions import db, bcrypt
from app.main.dto.user_dto import UserRegisterDto
from app.main.models.user import User
from app.main.utils import error_response, success_response
from app.main.schema.user_schema import UserLoginSchema

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app
from app.main.utils.email_utils import send_email
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import SQLAlchemyError

from app.main.schema.auth_schema import ForgotPasswordSchema, ResetPasswordSchema


class AuthService:

    @staticmethod
    def register_user(data: dict):
        try:
            # Check for existing user
            existing_user = User.query.filter((User.email == data['email']) | (User.phone == data['phone'])).first()

            if existing_user:
                return error_response("User with given email or phone already exists", 409)
            
            # Create User instance
            user = User(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                phone = data['phone'],
            )
            user.set_password(data['password'])


            # Assign role
            role = data.get('role')
            if 'role' and isinstance(role, str) and role.strip():
                print("role given")
                user.add_role(role.strip().lower())
            else:
                print("No role was given")
                user.add_role('tenant')

            db.session.add(user)
            db.session.commit()

            
            # Generate Tokens
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            return success_response(
                message = "User Registered Successfully",
                data = {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone": user.phone,
                        "role": [role.name for role in user.roles]
                    },
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
                status_code = 201
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            return error_response(f"Database error: {str(e)}", 500)
        
        except Exception as e:
            return error_response(f"Unexpected error: {str(e)}", 500)
        

    @staticmethod
    def login_user(data:dict):
        print("Entered login route")
        login_schema = UserLoginSchema()

        try:
            # Validate Input 
            validated_data = login_schema.load(data)
            print("login data validation done")
            print(validated_data)

            # Check if user exists already
            user = User.query.filter_by(email=validated_data['email']).first()

            if not user:
                return error_response("Invalid email or password", 401)

            # Verify password using bcrypt
            if not user.check_password(validated_data['password']):
                return error_response("Invalid email or password", 401)
            
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            return success_response(
                message="Login Successful",
                data = {
                    "user":{
                        "id":user.id,
                        "email":user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": [role.name for role in user.roles]
                    },
                    "access_token":access_token,
                    "refresh_token": refresh_token
                }
            )
            
        except Exception as e:
            return error_response(f"Login failed: {str(e)}", 500)
        
    

    @staticmethod
    def generate_reset_token(email):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(email, salt='password-reset-salt')
    

    @staticmethod
    def confirm_reset_token(token, expiration=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt='password-reset-salt',max_age=expiration)
            return email
        except SignatureExpired:
            return "expired"
        except BadSignature:
            return None
        
    @staticmethod
    def forgot_password(data):
        schema = ForgotPasswordSchema()
        validated_data = schema.load(data)
        email = validated_data['email']

        user = User.query.filter_by(email=email).first()
        if user:
            token = AuthService.generate_reset_token(email)
            print("Reset Token: ", token)
            reset_url = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"
            body = f"Hi {user.first_name},\n\nClick here to reset your password:\n{reset_url}\n\nThis link will expire in 1 hour."
            send_email("Password Reset", [email], body)
        
        return success_response({"message": "If user exists, email was sent"},200)
    

    @staticmethod
    def reset_password(data):
        schema = ResetPasswordSchema()
        validated_data = schema.load(data)

        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']
        token = validated_data.get("token")

        if new_password != confirm_password:
            return error_response("Passwords do not match", 400)

        email = AuthService.confirm_reset_token(token)
        if email == "expired":
            return {"message": "Token expired"}, 400
        if not email:
            return {"message": "Invalid token"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User not found"}, 404

        user.set_password(new_password)
        db.session.commit()
        return {"message": "Password reset successful"}, 200
    

    @staticmethod
    def get_current_user(user_id):
        user = User.query.get(user_id)

        if not user:
            return error_response("User not found", 404)
        
        return success_response(
            message="User fetched successfully",
            data={
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "roles": [role.name for role in user.roles]
            },
            status_code=200
        )