from marshmallow import Schema, fields

class WishlistSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Wishlist ID"})
    user_id = fields.Str(required=True, metadata={"description": "User ID"})
    product_id = fields.Str(required=True, metadata={"description": "Product ID"})
    created_at = fields.DateTime(required=True, metadata={"description": "Creation timestamp"})