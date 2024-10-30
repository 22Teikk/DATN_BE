from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.order_item_schema import OrderItemSchema
from src.containers.order_item_container import OrderItemContainer

def test_order_item_container():
    container = OrderItemContainer(RepositoryContainer())

    assert container.usecase is not None
