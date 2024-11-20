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
            "image_url": "http://94.237.64.46:5001/files/fast_food.png"
        },
        {
            "_id": get_new_uuid(),
            "name": "Cake",
            "image_url": "http://94.237.64.46:5001/files/cake.png"
        },
        {
            "_id": get_new_uuid(),
            "name": "Dessert",
            "image_url": "http://94.237.64.46:5001/files/dessert.png"
        },
        {
            "_id": get_new_uuid(),
            "name": "Coffee",
            "image_url": "http://94.237.64.46:5001/files/coffee.png"
        }
    ]
    container.usecase.upserts(data)
    print("Upsert completed")