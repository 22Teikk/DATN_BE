from src.containers.repository_container import RepositoryContainer
from src.containers.categories_container import CategoriesContainer
from src.domain.entities.utils import get_new_uuid


def test_categories_container():
    container = CategoriesContainer(repository_container=RepositoryContainer())
    assert container is not None
    data = [
        {
            "_id": get_new_uuid(),
            "category_name": "Fast Food",
        },
        {
            "_id": get_new_uuid(),
            "category_name": "WineAlcoholic beverages",
        },
        {
            "_id": get_new_uuid(),
            "category_name": "Juice",
        },
        {
            "_id": get_new_uuid(),
            "category_name": "Coffee",
        }
    ]
    container.usecase.upserts(data)