
from marshmallow import Schema, fields

class FeedbackSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Feedback ID"})
    start = fields.Int(required=True, metadata={"description": "Rating (1-5)"})
    title = fields.Str(required=False, metadata={"description": "Feedback title"})
    created_at = fields.DateTime(required=True, metadata={"description": "Feedback creation date"})
    product_id = fields.Str(required=True, metadata={"description": "Product ID"})
    user_id = fields.Str(required=True, metadata={"description": "User ID"})

    
