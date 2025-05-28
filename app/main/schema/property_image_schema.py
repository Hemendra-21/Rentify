from marshmallow import Schema, fields, validate

class PropertyImageSchema(Schema):
    id = fields.Int(dump_only=True)
    property_id = fields.Int(required=True)
    image_url = fields.Url(required=True, validate=validate.Length(max=512))
    uploaded_at = fields.DateTime(dump_only=True)
