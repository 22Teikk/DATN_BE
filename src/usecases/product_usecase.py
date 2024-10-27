
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.product_service import ProductService

class ProductUsecase(EntityUsecase):
    def __init__(self, product_service: ProductService):
        super().__init__(product_service)
    
