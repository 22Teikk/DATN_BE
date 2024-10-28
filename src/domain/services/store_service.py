
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.store_repository import StoreRepository


class StoreService(EntityServiceImpl):
    def __init__(self, store_repository: StoreRepository):
        super().__init__(store_repository)

    
