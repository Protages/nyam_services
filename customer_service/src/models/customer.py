from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database.db import Base


class CustomerTable(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(64), unique=True, nullable=True)
    name = Column(String(64), nullable=True)

    # One to Many
    addresses = relationship('CustomerAddressTable', back_populates='customer')
    
    def __str__(self) -> str:
        return f'customer {self.id}'
    

class CustomerAddressTable(Base):
    __tablename__ = 'customer_address'
    __table_args__ = (
        UniqueConstraint('address', 'customer_id', name='unique_address_customer_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(256), nullable=False)
    geolocation = Column(String, nullable=True)
    title = Column(String(64), nullable=True)
    icon = Column(String, nullable=True)

    # Many to One
    customer_id = Column(
        Integer,
        ForeignKey('customer.id', ondelete='CASCADE'),
        nullable=False
    )
    customer = relationship('CustomerTable', back_populates='addresses')

    def __str__(self) -> str:
        return f'customer_address {self.id}'
