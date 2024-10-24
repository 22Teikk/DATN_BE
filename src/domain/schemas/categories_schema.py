
from marshmallow import Schema, fields

class CategoriesSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "ID của danh mục"})
    category_name = fields.Str(required=True, metadata={"description": "Tên của danh mục"})