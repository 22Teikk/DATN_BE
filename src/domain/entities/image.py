
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Image(Base):
    __tablename__ = 'Image'
    __back_populated__ = "images"
    _id = Column(String(length=36) ,primary_key=True)
    url = Column(String(length=100))
    feedback_id = Column(String(length=36), nullable=True)
    product_id = Column(String(length=36), nullable=True)
    feedbacks = relationship("Feedback", back_populates='images')
    products = relationship("Product", back_populates='images')
    def __init__(self, _id: str, url: str, feedback_id: str = None, product_id: str = None):
        self._id = _id
        self.url = url
        self.feedback_id = feedback_id
        self.product_id = product_id
