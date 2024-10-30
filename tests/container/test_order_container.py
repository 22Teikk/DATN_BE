from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.order_schema import OrderSchema
from src.containers.order_container import OrderContainer

def test_order_container():
    container = OrderContainer(RepositoryContainer())

    assert container.usecase is not None
