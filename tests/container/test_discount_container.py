from src.containers.discount_container import DiscountContainer
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_new_uuid


def test_discounts_container():
    container = DiscountContainer(repository_container=RepositoryContainer())
    assert container is not None
    
    data = [
        {
            "_id": get_new_uuid(),
            "code": "SAVE10",
            "discount_percent": 10.0,
            "start_date": "2024-10-27T00:00:00",
            "end_date": "2024-11-27T00:00:00",
            "is_active": True
        },
        {
            "_id": get_new_uuid(),
            "code": "HALFPRICE",
            "discount_percent": 50.0,
            "start_date": "2024-11-01T00:00:00",
            "end_date": "2024-11-30T00:00:00",
            "is_active": True
        },
        {
            "_id": get_new_uuid(),
            "code": "FREESHIP",
            "discount_percent": 15.0,
            "start_date": "2024-12-01T00:00:00",
            "end_date": "2024-12-31T00:00:00",
            "is_active": False
        },
        {
            "_id": get_new_uuid(),
            "code": "BLACKFRI",
            "discount_percent": 20.0,
            "start_date": "2024-11-25T00:00:00",
            "end_date": "2024-11-26T00:00:00",
            "is_active": True
        }
    ]
    
    container.usecase.upserts(data)