
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.role_service_impl import RoleServiceImpl
from src.usecases.role_usecase import RoleUsecase

class RoleContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = RoleServiceImpl(repository_container.role_repository)
        self.usecase = RoleUsecase(service)

    
