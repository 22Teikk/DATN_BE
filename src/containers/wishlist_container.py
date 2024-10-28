
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.wishlist_service_impl import WishlistServiceImpl
from src.usecases.wishlist_usecase import WishlistUsecase

class WishlistContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = WishlistServiceImpl(repository_container.wishlist_repository)
        self.usecase = WishlistUsecase(service)

    
