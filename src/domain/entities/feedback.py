
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Feedback(Base):
    __tablename__ = 'Feedback'
    __back_populates__ = 'feedbacks'
    _id = Column(String(length=36) ,primary_key=True)
    star = Column(Integer, nullable=False)
    title = Column(String(length=255), nullable=True)
    created_at = Column(DateTime(), nullable=False)
    product_id = Column(String(length=36), ForeignKey('Product._id'))
    user_id = Column(String(length=36), ForeignKey('User._id'))
    products = relationship("Product", back_populates=__back_populates__)
    users = relationship("UserProfile", back_populates=__back_populates__)
    def __init__(self, _id: str):
        self._id = _id
    