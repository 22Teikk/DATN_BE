from src.containers.repository_container import RepositoryContainer
from src.containers.role_container import RoleContainer
from src.domain.entities.utils import get_new_uuid


def test_categories_container():
    container = RoleContainer(repository_container=RepositoryContainer())
    assert container is not None
    data = [
        {
            "_id": get_new_uuid(),
            "name": "Admin",
        },
        {
            "_id": get_new_uuid(),
            "name": "Client",
        },
        {
            "_id": get_new_uuid(),
            "name": "Employee",
        },
    ]
    container.usecase.upserts(data)
    print(container.usecase.find_by_query())