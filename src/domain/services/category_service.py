
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.category_repository import CategoryRepository


class CategoryService(EntityServiceImpl):
    def __init__(self, category_repository: CategoryRepository):
        super().__init__(category_repository)

    
