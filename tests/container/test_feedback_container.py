from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.feedback_schema import FeedbackSchema
from src.containers.feedback_container import FeedbackContainer

def test_feedback_container():
    container = FeedbackContainer(RepositoryContainer())

    assert container.usecase is not None
