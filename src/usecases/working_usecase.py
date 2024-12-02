
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.working_service import WorkingService

class WorkingUsecase(EntityUsecase):
    def __init__(self, working_service: WorkingService):
        super().__init__(working_service)
    
