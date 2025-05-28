from marshmallow import Schema, fields

class LoginDTO(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)