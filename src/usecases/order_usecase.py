
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.order_service import OrderService

class OrderUsecase(EntityUsecase):
    def __init__(self, order_service: OrderService):
        super().__init__(order_service)
    
