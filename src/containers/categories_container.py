
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.categories_service_impl import CategoriesServiceImpl
from src.usecases.categories_usecase import CategoriesUsecase

class CategoriesContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = CategoriesServiceImpl(repository_container.categories_repository)
        self.usecase = CategoriesUsecase(service)

    
