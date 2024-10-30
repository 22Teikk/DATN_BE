
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class OrderItem(Base):
    __tablename__ = 'OrderItem'
    ___back_populates__ = 'order_items'
    _id = Column(String(length=36) ,primary_key=True)
    product_id = Column(String(length=36), ForeignKey('Product._id'))
    order_id = Column(String(length=36), ForeignKey('Order._id'))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    orders = relationship("Order", back_populates=___back_populates__)
    products = relationship("Product", back_populates=___back_populates__)
    def __init__(
        self, 
        _id: str,
        product_id: str,
        order_id: str,
        quantity: int,
        price: float):
        self._id = _id
        self.product_id = product_id
        self.order_id = order_id
        self.quantity = quantity
        self.price = price
    
