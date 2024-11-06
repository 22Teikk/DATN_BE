
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.image_repository import ImageRepository


class ImageService(EntityServiceImpl):
    def __init__(self, image_repository: ImageRepository):
        super().__init__(image_repository)

    
