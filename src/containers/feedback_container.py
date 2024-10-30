
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.feedback_service_impl import FeedbackServiceImpl
from src.usecases.feedback_usecase import FeedbackUsecase

class FeedbackContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = FeedbackServiceImpl(repository_container.feedback_repository)
        self.usecase = FeedbackUsecase(service)

    
