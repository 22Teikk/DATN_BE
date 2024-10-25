from src.containers.category_container import CategoryContainer
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_new_uuid


def test_categories_container():
    container = CategoryContainer(repository_container=RepositoryContainer())
    assert container is not None
    data = [
        {
            "_id": get_new_uuid(),
            "name": "Fast Food",
        },
        {
            "_id": get_new_uuid(),
            "name": "WineAlcoholic beverages",
        },
        {
            "_id": get_new_uuid(),
            "name": "Juice",
        },
        {
            "_id": get_new_uuid(),
            "name": "Coffee",
        }
    ]
    container.usecase.upserts(data)