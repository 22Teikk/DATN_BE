from marshmallow import Schema, fields

class CategorySchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Category ID"})
    name = fields.Str(required=True, metadata={"description": "Category name"})
    image_url = fields.Str(required=True, metadata={"description": "Category image URL"})