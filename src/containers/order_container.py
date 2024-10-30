
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.order_service_impl import OrderServiceImpl
from src.usecases.order_usecase import OrderUsecase

class OrderContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = OrderServiceImpl(repository_container.order_repository)
        self.usecase = OrderUsecase(service)

    
