
import datetime
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
    users = relationship("UserProfile", back_populates='feedbacks')
    def __init__(
        self, 
        _id: str,
        star: int,
        title: str = None,
        created_at: datetime.datetime = None,
        product_id: str = None,
        user_id: str = None,):
        self._id = _id
        self.star = star
        self.title = title
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.product_id = product_id
        self.user_id = user_id