
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.working_service_impl import WorkingServiceImpl
from src.usecases.working_usecase import WorkingUsecase

class WorkingContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = WorkingServiceImpl(repository_container.working_repository)
        self.usecase = WorkingUsecase(service)

    
