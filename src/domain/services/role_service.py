
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.role_repository import RoleRepository


class RoleService(EntityServiceImpl):
    def __init__(self, role_repository: RoleRepository):
        super().__init__(role_repository)

    
