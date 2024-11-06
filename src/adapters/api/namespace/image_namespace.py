from flask_restx import Api
from src.containers.image_container import ImageContainer
from src.domain.schemas.image_schema import ImageSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class ImageNamespace(EntityNamespace):
    def __init__(
        self,
        container: ImageContainer,
        schema: ImageSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

