from flask_restx import Api
from src.containers.cart_container import CartContainer
from src.domain.schemas.cart_schema import CartSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class CartNamespace(EntityNamespace):
    def __init__(
        self,
        container: CartContainer,
        schema: CartSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

