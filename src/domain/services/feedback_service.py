
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.feedback_repository import FeedbackRepository


class FeedbackService(EntityServiceImpl):
    def __init__(self, feedback_repository: FeedbackRepository):
        super().__init__(feedback_repository)

    
