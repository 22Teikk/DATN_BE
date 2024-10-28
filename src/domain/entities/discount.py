import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Discount(Base):
    __tablename__ = 'Discount'
    __back_populates__ = 'discounts'
    _id = Column(String(length=36) ,primary_key=True, nullable=False)
    code = Column(String(length=10), nullable=False)
    discount_percent = Column(Float, nullable=False)
    start_date = Column(DateTime(), nullable=False)
    end_date = Column(DateTime(), nullable=False)
    is_active = Column(Boolean, nullable=False)
    products = relationship("Product", back_populates=__back_populates__)
    def __init__(self, _id: str, code: str, discount_percent: float, start_date: datetime.datetime = None, end_date: datetime.datetime = None, is_active: bool = True):
        self._id = _id
        self.code = code
        self.discount_percent = discount_percent
        self.start_date = start_date if isinstance(start_date, datetime.datetime) else datetime.datetime.fromisoformat(start_date)
        self.end_date = end_date if isinstance(end_date, datetime.datetime) else datetime.datetime.fromisoformat(end_date)
        self.is_active = is_active

