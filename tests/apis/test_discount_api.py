import os
from src.domain.entities.utils import get_current_timestamp_str, get_new_uuid
from src.domain.schemas.entity_schema import EntitySchema
from src.containers.discount_container import DiscountContainer
import requests
import pytest


@pytest.fixture(scope="module")
def discount_host():
    return 'http://localhost:5001'

@pytest.fixture(scope="module")
def discount_endpoint(discount_host):
    return f"{discount_host}/api/v1/discounts"  # Endpoint cho discounts

@pytest.fixture(scope="module")
def get_discount_id():
    return get_new_uuid()  # ID cho bản ghi giảm giá

@pytest.fixture(scope="module")
def discount_headers():
    return {"Content-Type": "application/json"}

def test_discount_api(discount_host, discount_endpoint, discount_headers):
    response = requests.get(discount_endpoint, headers=discount_headers)
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

def test_post_discount(discount_endpoint, discount_headers, get_discount_id):
    discount_data = {
        "_id": get_discount_id,
        "code": "SAVE10",
        "discount_percent": 10.0,
        "start_date": "2024-10-27T00:00:00",
        "end_date": "2024-11-27T00:00:00",
        "is_active": True
    }
    discount_find = requests.get(discount_endpoint + f"/{get_discount_id}", headers=discount_headers)
    print(">>>>>>>>>>>>>>> Response: " + str(discount_find.status_code))
    if discount_find.status_code != 200:
        response = requests.post(discount_endpoint, headers=discount_headers, json=discount_data)
        print("post", response.status_code, response.json())
        assert response.status_code == 201
    else:
        response = requests.post(discount_endpoint, headers=discount_headers, json=discount_data)
        print("post", response.status_code, response.json())
        assert response.status_code == 409

def test_put_discount(discount_endpoint, discount_headers, get_discount_id):
    discount_data = {
        "_id": get_discount_id,
        "code": "SAVE20",
        "discount_percent": 20.0,
        "start_date": "2024-10-27T00:00:00",
        "end_date": "2024-11-27T00:00:00",
        "is_active": True
    }
    
    response = requests.put(discount_endpoint + f'/{get_discount_id}', headers=discount_headers, json=discount_data)
    print("put", response.status_code, response.json())
    assert response.status_code == 200

    response_fail = requests.put(discount_endpoint + f'/{get_new_uuid()}', headers=discount_headers, json=discount_data)
    print("put", response_fail.status_code, response_fail.json())
    assert response_fail.status_code == 404

def test_get_discount(discount_host, discount_endpoint, get_discount_id, discount_headers):
    response = requests.get(discount_endpoint + f'/{get_discount_id}', headers=discount_headers)
    if response.status_code == 200:
        print("get", response.status_code, response.json())
        assert response.status_code == 200
    else:
        print("get", response.status_code, response.json())
        assert response.status_code == 404

def test_delete_discount(discount_host, discount_endpoint, discount_headers, get_discount_id):
    response = requests.delete(discount_endpoint + f'/{get_discount_id}', headers=discount_headers)
    if response.status_code == 204:
        print("delete", response.status_code, response.content)
        assert response.status_code == 204
    else:
        print("delete", response.status_code, response.json())
        assert response.status_code == 404
