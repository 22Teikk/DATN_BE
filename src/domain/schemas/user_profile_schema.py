from marshmallow import Schema, fields
from datetime import datetime

class UserProfileSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "User ID"})
    name = fields.Str(required=True, metadata={"description": "Name of the user"})
    username = fields.Str(required=True, metadata={"description": "Username of the user"})
    password = fields.Str(required=True, metadata={"description": "Password of the user"})
    address = fields.Str(required=True, metadata={"description": "Address of the user"})
    description = fields.Str(required=True, metadata={"description": "Description of the user"})
    role_id = fields.Str(required=True, metadata={"description": "Role ID of the user"})
    lat = fields.Float(required=True, metadata={"description": "Latitude of the user"})
    long = fields.Float(required=True, metadata={"description": "Longitude of the user"})
    email = fields.Email(required=True, metadata={"description": "Email of the user"})
    phone = fields.Str(required=True, metadata={"description": "Phone number of the user"})
    image_id = fields.Str(required=False, allow_none=True, metadata={"description": "Image ID of the user"})
    created_at = fields.DateTime(required=False, metadata={"description": "Creation date of the user"})