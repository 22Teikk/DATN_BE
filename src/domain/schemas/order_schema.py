
from marshmallow import Schema, fields

class OrderSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Order ID"})
    created_at = fields.Str(required=True, metadata={"description": "Order creation date"})
    status = fields.Str(required=True, metadata={"description": "Order status"})
    total = fields.Int(required=True, metadata={"description": "Order total"})
    lat = fields.Float(required=False, metadata={"description": "Order latitude"})
    long = fields.Float(required=False, metadata={"description": "Order longitude"})
    is_shipment = fields.Boolean(required=True, metadata={"description": "Is shipment required"})
    user_id = fields.Str(required=True, metadata={"description": "User ID"})
    payment_id = fields.Str(required=True, metadata={"description": "Payment ID"})
    description = fields.String(required=True, metadata={"description": "Description"})