from marshmallow import Schema, fields

class ProductSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Product ID"})
    name = fields.Str(required=True, metadata={"description": "Product name"})
    description = fields.Str(required=True, metadata={"description": "Product description"})
    price = fields.Float(required=True, metadata={"description": "Product price"})
    quantity_sold = fields.Int(required=True, metadata={"description": "Quantity sold"})
    is_sold = fields.Bool(required=True, metadata={"description": "Indicates if the product is sold"})
    total_time = fields.Int(required=True, metadata={"description": "Total time the product is available"})
    category_id = fields.Str(required=True, metadata={"description": "Category ID"})
    discount_id = fields.Str(required=False, allow_none=True, metadata={"description": "Discount ID (optional)"})