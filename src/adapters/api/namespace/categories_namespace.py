from flask_restx import Api
from src.containers.categories_container import CategoriesContainer
from src.domain.schemas.categories_schema import CategoriesSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class CategoriesNamespace(EntityNamespace):
    def __init__(
        self,
        container: CategoriesContainer,
        schema: CategoriesSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

