from sqlalchemy.orm import relationship
from src.domain.entities.utils import Base
from sqlalchemy import Column, DateTime, String, Float, Time

class Store(Base):
    __tablename__ = 'Store'
    __back_populates__ = 'stores'
    _id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    open_time = Column(String(30), nullable=False)
    close_time = Column(String(30), nullable=False)
    image_src = Column(String(100), nullable=False)
    open_day = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    
    users = relationship("UserProfile", back_populates=__back_populates__)
    def __init__(
        self, 
        _id: str,
        name: str,
        address: str,
        description: str,
        lat: float,
        long: float,
        open_time: str,
        close_time: str,
        open_day: str,
        phone: str,
        image_src: str,
        email: str
    ):
        self._id = _id
        self.name = name
        self.address = address
        self.description = description
        self.lat = lat
        self.long = long
        self.open_time = open_time
        self.close_time = close_time
        self.open_day = open_day
        self.phone = phone
        self.email = email
        self.image_src = image_src
