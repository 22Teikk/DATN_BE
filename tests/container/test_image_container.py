from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.image_schema import ImageSchema
from src.containers.image_container import ImageContainer

def test_image_container():
    container = ImageContainer(RepositoryContainer())

    assert container.usecase is not None
