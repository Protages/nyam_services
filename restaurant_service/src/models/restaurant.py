from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database.db import Base


class RestaurantTable(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    title = Column(String(64), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    is_open = Column(Boolean, default=False)

    # One to Many
    addresses = relationship('RestaurantAddressTable', back_populates='restaurant')
    dishes = relationship('DishTable', back_populates='restaurant')
    
    def __str__(self) -> str:
        return f'restaurant {self.id}'


class RestaurantAddressTable(Base):
    __tablename__ = 'restaurant_address'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(256), nullable=False)
    geolocation = Column(String, nullable=True)
    title = Column(String(64), nullable=True)

    # Many to One
    restaurant_id = Column(
        Integer,
        ForeignKey('restaurant.id', ondelete='CASCADE'),
        nullable=False
    )
    restaurant = relationship('RestaurantTable', back_populates='addresses')

    def __str__(self) -> str:
        return f'restaurant address {self.id}'
