import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base

class Discount(Base):
    __tablename__ = 'Discount'
    _id = Column(String(length=36) ,primary_key=True, nullable=False)
    code = Column(String(length=10), nullable=False)
    discount_percent = Column(Float, nullable=False)
    start_date = Column(DateTime(), nullable=False)
    end_date = Column(DateTime(), nullable=False)
    is_active = Column(Boolean, nullable=False)

    def __init__(self, _id: str, code: str, discount_percent: float, start_date: datetime.datetime = None, end_date: datetime.datetime = None, is_active: bool = True):
        self._id = _id
        self.code = code
        self.discount_percent = discount_percent
        self.start_date = start_date or datetime.datetime.utcnow()
        self.end_date = end_date or datetime.datetime.utcnow()
        self.is_active = is_active

