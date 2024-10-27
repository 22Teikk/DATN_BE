
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.product_repository import ProductRepository


class ProductService(EntityServiceImpl):
    def __init__(self, product_repository: ProductRepository):
        super().__init__(product_repository)

    
