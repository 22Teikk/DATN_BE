
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.order_item_service_impl import OrderItemServiceImpl
from src.usecases.order_item_usecase import OrderItemUsecase

class OrderItemContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = OrderItemServiceImpl(repository_container.order_item_repository)
        self.usecase = OrderItemUsecase(service)

    
