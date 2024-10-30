
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.order_item_repository import OrderItemRepository


class OrderItemService(EntityServiceImpl):
    def __init__(self, order_item_repository: OrderItemRepository):
        super().__init__(order_item_repository)

    
