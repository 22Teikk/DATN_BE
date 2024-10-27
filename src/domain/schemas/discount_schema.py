from marshmallow import Schema, fields

class DiscountSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Discount ID"})
    code = fields.Str(required=True, metadata={"description": "Discount code"})
    discount_percent = fields.Float(required=True, metadata={"description": "Discount percentage"})
    start_date = fields.DateTime(required=True, metadata={"description": "Discount start date"})
    end_date = fields.DateTime(required=True, metadata={"description": "Discount start date"})
    is_active = fields.Boolean(required=True, metadata={"description": "Is discount active"})
