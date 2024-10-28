
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.user_profile_repository import UserProfileRepository


class UserProfileService(EntityServiceImpl):
    def __init__(self, user_profile_repository: UserProfileRepository):
        super().__init__(user_profile_repository)

    
