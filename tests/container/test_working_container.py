from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.working_schema import WorkingSchema
from src.containers.working_container import WorkingContainer

def test_working_container():
    container = WorkingContainer(RepositoryContainer())

    assert container.usecase is not None
