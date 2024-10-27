from flask_restx import Api
from src.containers.product_container import ProductContainer
from src.domain.schemas.product_schema import ProductSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class ProductNamespace(EntityNamespace):
    def __init__(
        self,
        container: ProductContainer,
        schema: ProductSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

