from marshmallow import Schema, fields, validate, validates, ValidationError
# from app.main.models.user import UserRole 


# UserInputSchema - for user registration/login
class UserRegisterSchema(Schema):
    firstName = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    lastName = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Length(min=1, max=13))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6)) 
    role = fields.Str(required=False)

    # @validates('phone')
    # def validate_phone(self, value=None):
    #     print("validate_phone called with:", value)
    #     if value and not value.isdigit():
    #         raise ValidationError("Phone number must contain digits only")
        
# load_only=True; it keeps the password excluded from any output (security)
# Custom phone validation ensures it's numeric 




# UserOutputSchema - for sending user data to frontend/API calls
class UserOutputSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    phone = fields.Str()
    role = fields.Str()
    identity_verified = fields.Bool()
    profile_image = fields.Str(allow_none=True)
    is_active = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()



# -----------------------------
# User login schema
# -----------------------------
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))