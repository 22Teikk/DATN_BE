from src.domain.entities.product import Product
from src.domain.entities.user_profile import UserProfile
from src.domain.entities.wishlist import Wishlist
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid, obj_to_dict
from src.domain.schemas.wishlist_schema import WishlistSchema
from src.containers.wishlist_container import WishlistContainer

def test_wishlist_container():
    container = WishlistContainer(RepositoryContainer())

    assert container.usecase is not None
    # data = {
    #     "_id": get_new_uuid(),
    #     "user_id": "sdflkas123j",
    #     "product_id": "475612ed-03f7-4b42-954a-a48d81c44a07",
    #     "created_at": get_current_timestamp_str(),
    # }
    # container.usecase.insert(data)
    # assert container.usecase.find_by_id(data["_id"]) is not None

    session = container.usecase.get_session_manager()
    data = (session.query(Wishlist, Product, UserProfile)
            .join(Product, Wishlist.product_id == Product._id)
            .join(UserProfile, Wishlist.user_id == UserProfile._id)
            .first())
    wishlist = obj_to_dict(data[0])
    print(wishlist)

