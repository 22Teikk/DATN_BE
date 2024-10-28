import os
from src.domain.entities.utils import get_current_timestamp_str
from src.domain.schemas.entity_schema import EntitySchema
from src.containers.user_profile_container import UserProfileContainer
import requests
import pytest

@pytest.fixture(scope="module")
def host():
    return os.getenv("APP_HOST")

@pytest.fixture(scope="module")
def endpoint(host):
    return f"{host}/api/v1/user_profiles"


def test_user_profile_api(host, endpoint):
    headers = {"Content-Type": "application/json"}
    _id = "string"

    data = requests.get(f"{endpoint}/{_id}", headers=headers).json()
    print(data)