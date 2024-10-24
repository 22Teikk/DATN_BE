
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.categories_repository import CategoriesRepository


class CategoriesService(EntityServiceImpl):
    def __init__(self, categories_repository: CategoriesRepository):
        super().__init__(categories_repository)

    
