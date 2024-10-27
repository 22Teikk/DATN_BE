
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.product_service_impl import ProductServiceImpl
from src.usecases.product_usecase import ProductUsecase

class ProductContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = ProductServiceImpl(repository_container.product_repository)
        self.usecase = ProductUsecase(service)

    
