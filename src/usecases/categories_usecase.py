
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.categories_service import CategoriesService

class CategoriesUsecase(EntityUsecase):
    def __init__(self, categories_service: CategoriesService):
        super().__init__(categories_service)
    
