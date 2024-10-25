from flask_restx import Api
from src.containers.category_container import CategoryContainer
from src.domain.schemas.category_schema import CategorySchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class CategoryNamespace(EntityNamespace):
    def __init__(
        self,
        container: CategoryContainer,
        schema: CategorySchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)
