
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.wishlist_repository import WishlistRepository


class WishlistService(EntityServiceImpl):
    def __init__(self, wishlist_repository: WishlistRepository):
        super().__init__(wishlist_repository)

    
