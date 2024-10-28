
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.store_service import StoreService

class StoreUsecase(EntityUsecase):
    def __init__(self, store_service: StoreService):
        super().__init__(store_service)
    
