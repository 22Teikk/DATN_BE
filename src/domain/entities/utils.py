from datetime import datetime
import uuid
from flask_restx import fields as restx_fields
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import fields
import hashlib
from sqlalchemy.orm import object_mapper

Base = declarative_base()

def get_current_timestamp_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_date_str() -> str:
    return datetime.now().strftstr("%Y-%m-%d")

def get_current_timestamp():
    return datetime.now().timestamp()


def get_new_uuid():
    return str(uuid.uuid4())

def obj_to_dict(obj):
    return {col.key: getattr(obj, col.key) for col in object_mapper(obj).columns}

# Hàm chuyển đổi marshmallow fields thành flask-restx fields
def schema_to_restx_model(schema, name="Model", api=None):
    to_restx_fields = {}
    for field_name, field in schema.fields.items():
        if isinstance(field, fields.String):
            to_restx_fields[field_name] = restx_fields.String(
                required=field.required,
                description=field.metadata.get("description", ""),
            )
        elif isinstance(field, fields.Integer):
            to_restx_fields[field_name] = restx_fields.Integer(
                required=field.required,
                description=field.metadata.get("description", ""),
            )
        elif isinstance(field, fields.Boolean):
            to_restx_fields[field_name] = restx_fields.Boolean(
                required=field.required,
                description=field.metadata.get("description", ""),
            )
        elif isinstance(field, fields.Float):
            to_restx_fields[field_name] = restx_fields.Float(
                required=field.required,
                description=field.metadata.get("description", ""),
            )
        elif isinstance(field, fields.DateTime):
            to_restx_fields[field_name] = restx_fields.DateTime(
                required=field.required,
                description=field.metadata.get("description", ""),
            )
        elif isinstance(field, fields.List):
            to_restx_fields[field_name] = restx_fields.List(
                required=field.required,
                description=field.metadata.get("description", ""),
            )
        # raw
        elif isinstance(field, fields.Raw):
            to_restx_fields[field_name] = restx_fields.Raw(
                required=field.required,
                description=field.metadata.get("description", ""),
            )

    return api.model(name, to_restx_fields)


def get_md5_from_str(str_input: str):
    """
    Get the MD5 hash of a string.
    Args:
        str_input (str): The string to hash.
    """
    md5_hash = hashlib.md5()
    md5_hash.update(str_input.encode("utf-8"))
    return md5_hash.hexdigest()
