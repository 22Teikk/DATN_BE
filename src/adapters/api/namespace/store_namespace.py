from flask_restx import Api
from src.containers.store_container import StoreContainer
from src.domain.schemas.store_schema import StoreSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class StoreNamespace(EntityNamespace):
    def __init__(
        self,
        container: StoreContainer,
        schema: StoreSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

