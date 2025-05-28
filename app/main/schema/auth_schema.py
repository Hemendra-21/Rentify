from marshmallow import Schema, fields, validate

class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=5))


class ResetPasswordSchema(Schema):
    token = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=6))
    confirm_password = fields.String(required=True, validate=validate.Length(min=6))
