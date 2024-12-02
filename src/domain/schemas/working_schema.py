from marshmallow import Schema, fields

class WorkingSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Working ID"})
    user_id = fields.Str(required=True, metadata={"description": "Working ID"})
    order_id = fields.Str(required=True, metadata={"description": "Working ID"})
    type = fields.Str(required=True, metadata={"description": "Working ID"})
    date = fields.Str(required=True)