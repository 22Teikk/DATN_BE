
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.user_profile_service import UserProfileService

class UserProfileUsecase(EntityUsecase):
    def __init__(self, user_profile_service: UserProfileService):
        super().__init__(user_profile_service)
    
