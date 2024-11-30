import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Wishlist(Base):
    __tablename__ = 'Wishlist'
    __back_populates__ = 'wishlists'
    _id = Column(String(length=36) ,primary_key=True)
    user_id = Column(String(length=36), ForeignKey('User._id'))
    product_id = Column(String(length=36), ForeignKey('Product._id'))
    created_at = Column(String(length=100))
    products = relationship("Product", back_populates=__back_populates__)
    users = relationship("UserProfile", back_populates=__back_populates__)
    def __init__(
        self, 
        _id: str,
        user_id: str,
        product_id: str,
        created_at: str,):
        self._id = _id
        self.user_id = user_id
        self.product_id = product_id
        self.created_at = str