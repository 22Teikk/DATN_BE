
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.role_service import RoleService

class RoleUsecase(EntityUsecase):
    def __init__(self, role_service: RoleService):
        super().__init__(role_service)
    
