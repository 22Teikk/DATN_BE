import os
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.payment_method_schema import PaymentMethodSchema
from src.containers.payment_method_container import PaymentMethodContainer

def test_payment_method_container():
    container = PaymentMethodContainer(RepositoryContainer())
    assert container.usecase is not None
    host = os.getenv('APP_HOST')
    data = [
        {
            "_id": get_new_uuid(),
            "name": "COD",
            "image_url": f"{host}/files/bank_card.png"
        },
        {
            "_id": get_new_uuid(),
            "name": "Bank",
            "image_url": f"{host}/files/cod.jpeg"
        },
    ]
    container.usecase.upserts(data)
    print(container.usecase.find_by_query())
