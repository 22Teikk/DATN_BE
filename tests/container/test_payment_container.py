from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.payment_schema import PaymentSchema
from src.containers.payment_container import PaymentContainer

def test_payment_container():
    container = PaymentContainer(RepositoryContainer())

    assert container.usecase is not None
