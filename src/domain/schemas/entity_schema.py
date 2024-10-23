from marshmallow import Schema, fields
from src.domain.entities.utils import get_current_timestamp_str
from flask_restx import fields as restx_fields


class EntitySchema(Schema):
    _id = fields.Str(required=True, metadata={"description": "ID của đối tượng"})
    updated = fields.Str(
        load_default=get_current_timestamp_str(),
        metadata={"description": "Thời gian cập nhật"},
    )

    # Hàm chuyển đổi marshmallow fields thành flask-restx fields
    def schema_to_restx_model(name="Model", api=None):
        to_restx_fields = {}
        for field_name, field in fields.items():
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
            elif isinstance(field, fields.Raw):
                to_restx_fields[field_name] = restx_fields.Raw(
                    required=field.required,
                    description=field.metadata.get("description", ""),
                )
        return api.model(name, to_restx_fields)
