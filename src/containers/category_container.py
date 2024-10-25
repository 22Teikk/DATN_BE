
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.category_service_impl import CategoryServiceImpl
from src.usecases.category_usecase import CategoryUsecase

class CategoryContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = CategoryServiceImpl(repository_container.category_repository)
        self.usecase = CategoryUsecase(service)

    
