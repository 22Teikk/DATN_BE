from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.store_schema import StoreSchema
from src.containers.store_container import StoreContainer

def test_store_container():
    container = StoreContainer(RepositoryContainer())

    assert container.usecase is not None

    data = {
        "_id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Cửa Hàng Thực Phẩm Tươi Sống",
        "address": "123 Đường Thực Phẩm, Thành Phố HCM, Việt Nam",
        "description": "Cửa hàng cung cấp các loại thực phẩm tươi sống, an toàn và chất lượng.",
        "lat": 10.762622,
        "long": 106.660172,
        "open_time": "08:00:00",
        "close_time": "21:00:00",
        "image_src": "https://example.com/images/store.jpg",
        "open_day": "Thứ Hai - Chủ Nhật",
        "phone": "0901234567",
        "email": "contact@thucphamtuoi.com"
    }
    container.usecase.insert(data)

