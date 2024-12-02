
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.working_repository import WorkingRepository


class WorkingService(EntityServiceImpl):
    def __init__(self, working_repository: WorkingRepository):
        super().__init__(working_repository)

    
