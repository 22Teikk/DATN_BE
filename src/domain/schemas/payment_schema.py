
from marshmallow import Schema, fields

class PaymentSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Payment ID"})
    amount = fields.Float(required=True, metadata={"description": "Payment amount"})
    created_at = fields.DateTime(required=True, metadata={"description": "Payment creation date"})
    payment_method_id = fields.Str(required=True, metadata={"description": "Payment method ID"})