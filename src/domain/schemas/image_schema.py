
from marshmallow import Schema, fields

class ImageSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Image ID"})
    url = fields.Str(required=True, metadata={"description": "Image URL"})
    feedback_id = fields.Str(required=False, metadata={"description": "Feedback ID"})
    product_id = fields.Str(required=False, metadata={"description": "Product ID"})