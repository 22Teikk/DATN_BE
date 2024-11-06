
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.image_service_impl import ImageServiceImpl
from src.usecases.image_usecase import ImageUsecase

class ImageContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = ImageServiceImpl(repository_container.image_repository)
        self.usecase = ImageUsecase(service)

    
