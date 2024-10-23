from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.containers.repository_container import RepositoryContainer
from src.usecases.entity_usecase import EntityUsecase


class EntityContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = EntityServiceImpl(repository_container.entity_repository)
        self.usecase = EntityUsecase(service)
