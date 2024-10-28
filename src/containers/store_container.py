
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.store_service_impl import StoreServiceImpl
from src.usecases.store_usecase import StoreUsecase

class StoreContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = StoreServiceImpl(repository_container.store_repository)
        self.usecase = StoreUsecase(service)

    
