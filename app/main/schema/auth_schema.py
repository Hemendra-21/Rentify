from marshmallow import Schema, fields # type: ignore

# UserLoginSchema
class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
