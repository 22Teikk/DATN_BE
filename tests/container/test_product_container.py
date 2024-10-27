from src.containers.product_container import ProductContainer
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_new_uuid
from src.domain.schemas.product_schema import ProductSchema


def test_product_container():
    container = ProductContainer(RepositoryContainer())

    assert container.usecase is not None

    # Xóa sản phẩm nếu đã tồn tại
    container.usecase.delete("1")  # Thay "product_id_example" bằng ID sản phẩm thực tế nếu cần

    # Dữ liệu mẫu cho sản phẩm
    product_data = ProductSchema().load({
        "_id": get_new_uuid(),
        "name": "Sample Product",
        "description": "This is a sample product.",
        "price": 19.99,
        "feedback_id": None,  # Nếu có liên kết phản hồi, sử dụng ID thực tế
        "quantity_sold": 0,
        "is_sold": False,
        "total_time": 30,
        "category_id": "1",  # Thay bằng ID danh mục thực tế
        "discount_id": None,  # Nếu có giảm giá, sử dụng ID thực tế
    })
    product_id = product_data.get("_id")

    # Tạo một sản phẩm mới
    container.usecase.insert(product_data)

    # Xác nhận sản phẩm đã được tạo
    assert container.usecase.find_by_id(product_id) is not None

    # Cập nhật một số thông tin sản phẩm
    container.usecase.upserts(
        datas=[ProductSchema().load({
            "_id": product_id,
            "name": "Sample Product Updated",
            "description": "This is an updated sample product.",
            "price": 24.99,
            "feedback_id": None,  # Nếu cần liên kết phản hồi, sử dụng ID thực tế
            "quantity_sold": 10,
            "is_sold": True,
            "total_time": 60,
            "category_id": "0374dc8b-a5c1-4ebe-a5c7-a2be1375e080",  # Thay bằng ID danh mục thực tế
            "discount_id": None,  # Nếu có giảm giá, sử dụng ID thực tế
        })]
    )

    # Xác nhận thông tin sản phẩm đã được cập nhật
    updated_product = container.usecase.find_by_id(product_id)
    print( ">>>>>>>>>>>>>>>>>>>>>>: ",  str(updated_product),  str(type(updated_product)))
    data = ProductSchema().dump(updated_product)
    print("DKKHJFGDHJSKGFKJDHS: " ,data)
    print("DFGHJKHGFKJDHS: " , type(data))
    assert data["name"] == "Sample Product Updated"
    assert data["price"] == 24.99
    assert data["quantity_sold"] == 10
    assert data["is_sold"] is True

    # Kiểm tra xem sản phẩm có tồn tại hay không
    assert not container.usecase.find_by_id(product_id) is None

    # Lấy tất cả sản phẩm và in ra
    products = container.usecase.find_by_query()
    print(products)
