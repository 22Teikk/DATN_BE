from sqlalchemy import Row
from src.domain.schemas.category_schema import CategorySchema
from src.domain.entities.category import Category
from src.domain.entities.product import Product
from src.containers.product_container import ProductContainer
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_new_uuid
from src.domain.schemas.product_schema import ProductSchema
from sqlalchemy.orm import object_mapper


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
    data_list = ProductSchema().dump(updated_product)
    print("DKKHJFGDHJSKGFKJDHS: " ,data_list)
    print("DFGHJKHGFKJDHS: " , type(data_list))
    assert data_list["name"] == "Sample Product Updated"
    assert data_list["price"] == 24.99
    assert data_list["quantity_sold"] == 10
    assert data_list["is_sold"] is True

    # Kiểm tra xem sản phẩm có tồn tại hay không
    assert not container.usecase.find_by_id(product_id) is None

    # Lấy tất cả sản phẩm và in ra
    products = container.usecase.find_by_query()
    print(products)

    session = container.usecase.get_session_manager()
    # Dành cho việc lấy 1 đối tượng
    result : Row = session.query(Product, Category).join(Category, Product.category_id == Category._id).first()
    value1 = Product(**ProductSchema().load(to_dict(result[0])))
    value2 = Category(**CategorySchema().load(to_dict(result[1])))

    print(">>>>>>>>>>>>>>>>>>>>>>: ",  type(value1))
    print(">>>>>>>>>>>>>>>>>>>>>>: ",  value2.name)

    # Dành cho việc lấy ra danh sách đối tượng
    results = session.query(Product, Category).join(Category, Product.category_id == Category._id).all()

    # Lưu danh sách các kết quả dưới dạng dictionary hoặc đối tượng
    data_list = []
    for product, category in results:
        value1 = Product(**ProductSchema().load(to_dict(product)))
        value2 = Category(**CategorySchema().load(to_dict(category)))
        
        data_list.append({
            "product": value1,
            "category": value2
        })

    # Kiểm tra kết quả
    for item in data_list:
        print("Product:", item["product"].name)
        print("Category:", item["category"].name)

def to_dict(obj):
    return {col.key: getattr(obj, col.key) for col in object_mapper(obj).columns}