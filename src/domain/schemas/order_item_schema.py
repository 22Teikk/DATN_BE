
from marshmallow import Schema, fields

class OrderItemSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "OrderItem ID"})
    quantity = fields.Int(required=True, metadata={"description": "Quantity of the product"})
    product_id = fields.Str(required=True, metadata={"description": "Product ID"})
    order_id = fields.Str(required=True, metadata={"description": "Order ID"})
    price = fields.Float(required=True, metadata={"description": "Price of the product"})