from marshmallow import Schema, fields

class CartSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Cart ID"})
    user_id = fields.Str(required=True, metadata={"description": "User ID"})
    product_id = fields.Str(required=True, metadata={"description": "Product ID"})
    created_at = fields.Str(required=True, metadata={"description": "Creation timestamp"})
    quantity = fields.Int(required=True, metadata={"description": "Product quantity"})