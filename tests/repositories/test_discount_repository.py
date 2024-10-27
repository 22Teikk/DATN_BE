from src.domain.entities.utils import get_current_timestamp_str
from src.domain.schemas.discount_schema import DiscountSchema
from src.adapters.repositories.discount_repository import DiscountRepository

def test_discount_repository():
    discount_repository = DiscountRepository()
    assert discount_repository is not None
