
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.user_profile_service_impl import UserProfileServiceImpl
from src.usecases.user_profile_usecase import UserProfileUsecase

class UserProfileContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = UserProfileServiceImpl(repository_container.user_profile_repository)
        self.usecase = UserProfileUsecase(service)

    
