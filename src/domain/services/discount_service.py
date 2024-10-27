
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.discount_repository import DiscountRepository


class DiscountService(EntityServiceImpl):
    def __init__(self, discount_repository: DiscountRepository):
        super().__init__(discount_repository)

    
