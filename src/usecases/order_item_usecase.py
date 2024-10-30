
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.order_item_service import OrderItemService

class OrderItemUsecase(EntityUsecase):
    def __init__(self, order_item_service: OrderItemService):
        super().__init__(order_item_service)
    
