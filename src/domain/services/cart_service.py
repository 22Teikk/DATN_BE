
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.cart_repository import CartRepository


class CartService(EntityServiceImpl):
    def __init__(self, cart_repository: CartRepository):
        super().__init__(cart_repository)

    
