from marshmallow import Schema, fields

class PaymentMethodSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "PaymentMethod ID"})
    name = fields.Str(required=True, metadata={"description": "PaymentMethod name"})
    image_url = fields.Str(required=True, metadata={"description": "PaymentMethod Image URL"})