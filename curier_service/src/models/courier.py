from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database.db import Base


class CourierTable(Base):
    __tablename__ = 'courier'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    is_work = Column(Boolean, default=False, nullable=False)
    is_free = Column(Boolean, default=False, nullable=False)
    photo = Column(String, nullable=True)

    def __str__(self) -> str:
        return f'courier {self.id}'
