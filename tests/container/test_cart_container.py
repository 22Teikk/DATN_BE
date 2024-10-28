from src.domain.entities.cart import Cart
from src.domain.entities.product import Product
from src.domain.entities.user_profile import UserProfile
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid, obj_to_dict
from src.domain.schemas.cart_schema import CartSchema
from src.containers.cart_container import CartContainer

def test_cart_container():
    container = CartContainer(RepositoryContainer())

    assert container.usecase is not None

    data = {
        "_id": get_new_uuid(),
        "user_id": "sdflkas123j",
        "product_id": "475612ed-03f7-4b42-954a-a48d81c44a07",
        "created_at": get_current_timestamp_str(),
        "quantity": 1,  # Assuming there's a product with ID "475612ed-03f7-4b42-954a-a48d81c44a07"
    }
    container.usecase.insert(data)
    assert container.usecase.find_by_id(data["_id"]) is not None

    session = container.usecase.get_session_manager()
    data = (session.query(Cart, Product, UserProfile)
            .join(Product, Cart.product_id == Product._id)
            .join(UserProfile, Cart.user_id == UserProfile._id)
            .first())
    cart = obj_to_dict(data[0])
    print(cart)
