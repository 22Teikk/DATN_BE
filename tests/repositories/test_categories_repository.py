from src.domain.entities.utils import get_current_timestamp_str

from src.domain.schemas.categories_schema import CategoriesSchema
from src.adapters.repositories.categories_repository import CategoriesRepository

def test_categories_repository():
    categories_repository = CategoriesRepository()
    assert categories_repository is not None
