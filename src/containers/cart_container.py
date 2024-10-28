
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.cart_service_impl import CartServiceImpl
from src.usecases.cart_usecase import CartUsecase

class CartContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = CartServiceImpl(repository_container.cart_repository)
        self.usecase = CartUsecase(service)

    
