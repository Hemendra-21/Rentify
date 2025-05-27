import bcrypt
from app.main.extensions import db
from app.main.dto.user_dto import UserRegisterDto
from app.main.models.user import User
from app.main.utils import error_response, success_response

from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import SQLAlchemyError



class AuthService:

    @staticmethod
    def register_user(data: dict):
        try:
            # Validate Incoming data
            dto = UserRegisterDto(**data)

            # Check for existing user
            existing_user = User.query.filter((User.email == dto.email) | (User.phone == dto.phone)).first()

            if existing_user:
                return error_response("User with given email or phone already exists", 409)
            
            # Hash password using bcrypt
            hashed_password = bcrypt.hashpw(dto.password.encode('utf-8'), bcrypt.gensalt())

            # Create User instance
            user = User(
                first_name = dto.first_name,
                last_name = dto.last_name,
                email = dto.email,
                phone = dto.phone,
                role = dto.role,
                password_hash =  hashed_password.decode('utf-8')
            )

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
                        "role": user.role.value
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