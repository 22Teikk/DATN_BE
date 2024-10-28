from flask_restx import Api
from src.containers.wishlist_container import WishlistContainer
from src.domain.schemas.wishlist_schema import WishlistSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class WishlistNamespace(EntityNamespace):
    def __init__(
        self,
        container: WishlistContainer,
        schema: WishlistSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

