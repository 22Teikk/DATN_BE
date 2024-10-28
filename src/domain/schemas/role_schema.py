
from marshmallow import Schema, fields

class RoleSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Role ID"})
    name = fields.Str(required=True, metadata={"description": "Role name"})