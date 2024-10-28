import os
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.entity_schema import EntitySchema
from src.containers.role_container import RoleContainer
import requests
import pytest

@pytest.fixture(scope="module")
def host():
    return 'http://localhost:5001'

@pytest.fixture(scope="module")
def get_id():
    return "1"

@pytest.fixture(scope="module")
def endpoint(host):
    return f"{host}/api/v1/roles"

@pytest.fixture(scope="module")
def headers():
    return {"Content-Type": "application/json"}

def test_role_api(host, endpoint, headers):
    response = requests.get(endpoint, headers=headers)
    print("GET", response.status_code, response.content)
    if response.status_code == 200:
        print("get", response.status_code, response.json())
        assert response.status_code == 200
    elif response.status_code == 404:
        print("get", response.status_code, response.json())
        assert response.status_code == 404
    else:
        print('get', response.status_code, response.json())
        assert response.status_code == 401

def test_post_role(endpoint, headers, get_id):
    role_data = {
        "_id": get_id,
        "name": "Test role"
    }
    role_find = requests.get(endpoint + f"/{get_id}", headers=headers)
    print( ">>>>>>>>>>>>>>> Response: " + str( role_find.status_code))
    if role_find.status_code != 200:
        response = requests.post(endpoint, headers=headers, json=role_data)
        print("post", response.status_code, response.json())
        assert response.status_code == 201
    else:
        response = requests.post(endpoint, headers=headers, json=role_data)
        print("post", response.status_code, response.json())
        assert response.status_code == 409

def test_put_role(endpoint, headers, get_id):
    role_data = {
        "_id": get_id,
        "name": "Updated role"
    }
    
    response = requests.put(endpoint + f'/{get_id}', headers=headers, json=role_data)
    print("put", response.status_code, response.json())
    assert response.status_code == 200

    response_fail = requests.put(endpoint + f'/{get_new_uuid()}', headers=headers, json=role_data)
    print("put", response_fail.status_code, response.json())
    assert response_fail.status_code == 404
def test_get_role(host, endpoint, get_id, headers):
    response = requests.get(endpoint + f'/{get_id}', headers=headers)
    if response.status_code == 200:
        print("get", response.status_code, response.json())
        assert response.status_code == 200
    else:
        print("get", response.status_code, response.json())
        assert response.status_code == 404


def test_delete_role(host, endpoint, headers, get_id):
    response = requests.delete(endpoint + f'/{get_id}', headers=headers)
    if response.status_code == 204:
        print("delete", response.status_code, response.content)
        assert response.status_code == 204
    else:
        print("delete", response.status_code, response.json())
        assert response.status_code == 404