from src.containers.repository_container import RepositoryContainer
from src.adapters.services.discount_service_impl import DiscountServiceImpl
from src.usecases.discount_usecase import DiscountUsecase

class DiscountContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = DiscountServiceImpl(repository_container.discount_repository)
        self.usecase = DiscountUsecase(service)

    
