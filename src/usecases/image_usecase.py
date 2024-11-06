
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.image_service import ImageService

class ImageUsecase(EntityUsecase):
    def __init__(self, image_service: ImageService):
        super().__init__(image_service)
    
