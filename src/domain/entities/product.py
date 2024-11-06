from sqlalchemy import Column, ForeignKey, String, DECIMAL, Boolean, Integer
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Product(Base):
    __tablename__ = 'Product'  # Tên bảng trong cơ sở dữ liệu
    __back_populates__ = 'products'  # Tên trư��ng liên kết với bảng products
    # Các trường của bảng products
    _id = Column(String(length=36), primary_key=True, nullable=False)  # ID sản phẩm
    name = Column(String(length=100), nullable=False)  # Tên sản phẩm
    description = Column(String(length=200), nullable=False)  # Mô tả sản phẩm
    price = Column(DECIMAL(10, 2), nullable=False)  # Giá sản phẩm
    quantity_sold = Column(Integer, nullable=False)  # Số lượng đã bán
    is_sold = Column(Boolean, nullable=False)  # Trạng thái đã bán
    total_time = Column(Integer, nullable=False)  # Tổng thời gian (có thể hiểu là thời gian sản phẩm được bán)
    category_id = Column(String(length=36), ForeignKey('Category._id'), nullable=False)  # ID danh mục, liên kết với bảng categories
    discount_id = Column(String(length=36), ForeignKey('Discount._id'), nullable=True)  # ID giảm giá, liên kết với bảng discounts

    # Quan hệ với bảng feedback, categories và discounts
    feedback = relationship("Feedback", back_populates=__back_populates__)  # Liên kết với bảng Feedback
    categories = relationship("Category", back_populates=__back_populates__)  # Liên kết với bảng Category
    discounts = relationship("Discount", back_populates=__back_populates__)  # Liên kết với bảng Discount
    wishlists = relationship("Wishlist", back_populates=__back_populates__)  # Liên kết với bảng Wishlist
    carts = relationship("Cart", back_populates=__back_populates__)  # Liên kết với bảng Cart
    order_items = relationship("OrderItem", back_populates=__back_populates__)  # Liên kết với bảng OrderItem
    feedbacks = relationship("Feedback", back_populates=__back_populates__)  # Liên kết với bảng Feedback
    images = relationship("Image", back_populates=__back_populates__)
    def __init__(self, _id: str, name: str, description: str, price: float,
        quantity_sold: int, is_sold: bool, total_time: int,
        category_id: str, feedback_id: str = None, discount_id: str = None):
        self._id = _id
        self.name = name
        self.description = description
        self.price = price
        self.quantity_sold = quantity_sold
        self.is_sold = is_sold
        self.total_time = total_time
        self.category_id = category_id
        self.discount_id = discount_id

