from flask_restx import Api
from src.containers.order_item_container import OrderItemContainer
from src.domain.schemas.order_item_schema import OrderItemSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class OrderItemNamespace(EntityNamespace):
    def __init__(
        self,
        container: OrderItemContainer,
        schema: OrderItemSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

