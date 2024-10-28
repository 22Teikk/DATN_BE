
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.cart_service import CartService

class CartUsecase(EntityUsecase):
    def __init__(self, cart_service: CartService):
        super().__init__(cart_service)
    
