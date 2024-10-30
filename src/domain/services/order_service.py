
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.order_repository import OrderRepository


class OrderService(EntityServiceImpl):
    def __init__(self, order_repository: OrderRepository):
        super().__init__(order_repository)

    
