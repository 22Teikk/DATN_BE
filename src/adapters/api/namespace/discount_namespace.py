from flask_restx import Api
from src.containers.discount_container import DiscountContainer
from src.domain.schemas.discount_schema import DiscountSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class DiscountNamespace(EntityNamespace):
    def __init__(
        self,
        container: DiscountContainer,
        schema: DiscountSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

