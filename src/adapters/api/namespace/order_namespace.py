from flask_restx import Api
from src.containers.order_container import OrderContainer
from src.domain.schemas.order_schema import OrderSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class OrderNamespace(EntityNamespace):
    def __init__(
        self,
        container: OrderContainer,
        schema: OrderSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)
