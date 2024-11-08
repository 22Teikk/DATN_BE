from src.domain.entities.user_profile import UserProfile
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.user_profile_schema import UserProfileSchema
from src.containers.user_profile_container import UserProfileContainer

def test_user_profile_container():
    container = UserProfileContainer(RepositoryContainer())

    assert container.usecase is not None

    session = container.usecase.get_session_manager()
    result = session.query(UserProfile).filter_by(_id="sdflkas123j").first()
    print(result)
    print(result.stores.name)