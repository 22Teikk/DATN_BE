from marshmallow import Schema, fields

class StoreSchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Store ID"})
    name = fields.Str(required=True, metadata={"description": "Name of the store"})
    address = fields.Str(required=True, metadata={"description": "Address of the store"})
    description = fields.Str(required=True, metadata={"description": "Description of the store"})
    lat = fields.Float(required=True, metadata={"description": "Latitude of the store"})
    long = fields.Float(required=True, metadata={"description": "Longitude of the store"})
    open_time = fields.Time(required=True, metadata={"description": "Opening time of the store"})
    close_time = fields.Time(required=True, metadata={"description": "Closing time of the store"})
    image_src = fields.Str(required=True, metadata={"description": "Image src associated with the store"})
    open_day = fields.Str(required=True, metadata={"description": "Days the store is open"})
    phone = fields.Str(required=True, validate=lambda p: len(p) == 10, metadata={"description": "Phone number of the store"})
    email = fields.Email(required=True, metadata={"description": "Email address of the store"})