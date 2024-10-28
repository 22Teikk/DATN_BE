
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.wishlist_service import WishlistService

class WishlistUsecase(EntityUsecase):
    def __init__(self, wishlist_service: WishlistService):
        super().__init__(wishlist_service)
    
