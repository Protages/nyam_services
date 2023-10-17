from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from src.database.db import Base


dish_category_dish = Table(
    'dish_category_dish',
    Base.metadata,
    Column('dish_id', ForeignKey('dish.id', ondelete='CASCADE')),
    Column('dish_category_id', ForeignKey('dish_category.id', ondelete='CASCADE')),
    UniqueConstraint('dish_id', 'dish_category_id', name='unique_dish_id_dish_category_id')
)


class DishTable(Base):
    __tablename__ = 'dish'
    __table_args__ = (
        UniqueConstraint('title', 'restaurant_id', name='unique_title_restaurant_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    price = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)
    visible = Column(Boolean, default=True)
    image = Column(String, nullable=True)

    # Many to One
    restaurant_id = Column(
        Integer,
        ForeignKey('restaurant.id', ondelete='CASCADE'),
        nullable=False
    )
    restaurant = relationship('RestaurantTable', back_populates='dishes')

    # Many to Many
    categories = relationship(
        'DishCategoryTable',
        secondary=dish_category_dish,
        back_populates='dishes',
        # стоит по умолчанию, тогда автоматом не будет подтягивать категории, 
        # пока мы явно не сформируем запрос с требованием подтянуть их
        lazy='select',
        # тогда ВСЕГДА будет подтягивать категории отдельным запросом, даже если они нам не нужны
        # lazy='selectin'
    )

    def __str__(self) -> str:
        return f'dish {self.id}'


class DishCategoryTable(Base):
    __tablename__ = 'dish_category'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), nullable=False, unique=True)

    # Many to Many
    dishes = relationship(
        'DishTable', secondary=dish_category_dish, back_populates='categories'
    )

    def __str__(self) -> str:
        return f'dish category {self.id}'
