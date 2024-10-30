
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.feedback_service import FeedbackService

class FeedbackUsecase(EntityUsecase):
    def __init__(self, feedback_service: FeedbackService):
        super().__init__(feedback_service)
    
