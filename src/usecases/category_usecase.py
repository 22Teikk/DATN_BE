
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.category_service import CategoryService

class CategoryUsecase(EntityUsecase):
    def __init__(self, category_service: CategoryService):
        super().__init__(category_service)
    
