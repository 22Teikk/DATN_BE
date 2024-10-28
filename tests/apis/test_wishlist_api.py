import os
from src.domain.entities.utils import get_current_timestamp_str
from src.domain.schemas.entity_schema import EntitySchema
from src.containers.wishlist_container import WishlistContainer
import requests
import pytest

@pytest.fixture(scope="module")
def host():
    return os.getenv("APP_HOST")

@pytest.fixture(scope="module")
def endpoint(host):
    return f"{host}/api/v1/wishlists"


def test_wishlist_api(host, endpoint):
    headers = {"Content-Type": "application/json"}
    _id = "1"

    data = {"_id": _id, "created_at": get_current_timestamp_str()}
