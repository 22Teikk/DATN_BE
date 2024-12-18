import pytest
import requests
from marshmallow import ValidationError

from src.domain.entities.utils import get_new_uuid

@pytest.fixture(scope="module")
def host():
    return 'http://localhost:5001'

@pytest.fixture(scope="module")
def endpoint(host):
    return f"{host}/api/v1/products"  # Cập nhật endpoint cho products

@pytest.fixture(scope="module")
def get_id():
    return '1'

@pytest.fixture(scope="module")
def headers():
    return {"Content-Type": "application/json"}

def test_product_api(host, endpoint, headers):
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

def test_post_product(endpoint, headers, get_id):
    product_data = {
        "_id": get_id,
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 19.99,
        "feedback_id": None,  # Nếu có phản hồi, sử dụng ID thực tế
        "quantity_sold": 0,
        "is_sold": False,
        "total_time": 30,
        "category_id": "1",  # Thay bằng ID danh mục thực tế
        "discount_id": None,  # Nếu có giảm giá, sử dụng ID thực tế
    }
    
    product_find = requests.get(endpoint + f"/{get_id}", headers=headers)
    print(">>>>>>>>>>>>>>> Response: " + str(product_find.status_code))
    
    if product_find.status_code != 200:
        response = requests.post(endpoint, headers=headers, json=product_data)
        print("post", response.status_code, response.json())
        assert response.status_code == 201
    else:
        response = requests.post(endpoint, headers=headers, json=product_data)
        print("post", response.status_code, response.json())
        assert response.status_code == 409

def test_put_product(endpoint, headers, get_id):
    product_data = {
        "_id": get_id,
        "name": "Updated Test Product",
        "description": "This is an updated test product.",
        "price": 24.99,
        "feedback_id": None,  # Nếu có phản hồi, sử dụng ID thực tế
        "quantity_sold": 10,
        "is_sold": True,
        "total_time": 60,
        "category_id": "1",  # Thay bằng ID danh mục thực tế
        "discount_id": None,  # Nếu có giảm giá, sử dụng ID thực tế
    }
    
    response = requests.put(endpoint + f'/{get_id}', headers=headers, json=product_data)
    print("put", response.status_code, response.json())
    assert response.status_code == 200

    response_fail = requests.put(endpoint + f'/{get_new_uuid()}', headers=headers, json=product_data)
    print("put", response_fail.status_code, response.json())
    assert response_fail.status_code == 404

def test_get_product(host, endpoint, get_id, headers):
    response = requests.get(endpoint + f'/{get_id}', headers=headers)
    if response.status_code == 200:
        print("get", response.status_code, response.json())
        assert response.status_code == 200
    else:
        print("get", response.status_code, response.json())
        assert response.status_code == 404

def test_delete_product(host, endpoint, headers, get_id):
    response = requests.delete(endpoint + f'/{get_id}', headers=headers)
    if response.status_code == 204:
        print("delete", response.status_code, response.content)
        assert response.status_code == 204
    else:
        print("delete", response.status_code, response.json())
        assert response.status_code == 404
