
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.discount_service import DiscountService

class DiscountUsecase(EntityUsecase):
    def __init__(self, discount_service: DiscountService):
        super().__init__(discount_service)
    
