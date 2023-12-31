from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.courier import (
    CourierUpdateSchema, 
    CourierCreateSchema, 
    CourierSchema, 
)
from src.schemas.login import CourierForGetTokenSchema
from src.repositories.courier.abstract import CourierAbcRepo
from src.core.exceptions import ObjectDoesNotExistException
from src.models.courier import CourierTable
from src.utils.validators import validate_courier_exist


class CourierSQLAlchemyRepo(CourierAbcRepo):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> CourierSchema:
        stmt = (
            select(CourierTable)
            .where(CourierTable.id == id)
        )
        res = await self.session.execute(stmt)
        courier_db = res.fetchone()
        if not courier_db:
            raise ObjectDoesNotExistException(obj_name='courier', obj_id=id)
        
        courier_schema = CourierSchema.model_validate(courier_db[0])
        return courier_schema

    async def get_by_phone_number(self, phone_number: str) -> CourierForGetTokenSchema:
        stmt = select(CourierTable).where(CourierTable.phone_number==phone_number)
        res = await self.session.execute(stmt)
        courier_db = res.fetchone()
        if not courier_db:
            raise ObjectDoesNotExistException(obj_name='courier')
        
        courier_schema = CourierForGetTokenSchema.model_validate(courier_db[0])
        return courier_schema

    async def get_all(self) -> list[CourierSchema]:
        stmt = select(CourierTable)
        res = await self.session.execute(stmt)
        courieres_schema = [
            CourierSchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return courieres_schema
    
    async def update(self, id: int, update_data: CourierUpdateSchema) -> CourierSchema:
        data_dict: dict = jsonable_encoder(update_data, exclude_unset=True)

        # С помощью `returning` делаем апдейт + получаем обновленную запись одним запросом
        if data_dict:
            stmt = (
                update(CourierTable)
                .where(CourierTable.id == id)
                .values(data_dict)
                .returning('*')
            )
        else:
            stmt = (
                select(CourierTable)
                .where(CourierTable.id == id)
            )

        res = await self.session.execute(stmt)
        courier_db = res.fetchone() if data_dict else res.scalar_one()

        if not courier_db:
            raise ObjectDoesNotExistException(obj_name='courier', obj_id=id)

        courier_schema = CourierSchema.model_validate(courier_db)
        return courier_schema
    
    async def create(self, create_data: CourierCreateSchema) -> CourierSchema:
        data_dict: dict = jsonable_encoder(create_data, exclude_unset=True)

        hashed_password: str = create_data.password
        data_dict['password'] = hashed_password

        stmt = insert(CourierTable).values(**data_dict).returning('*')
        res = await self.session.execute(stmt)
        courier_db = res.fetchone()

        courier_schema = CourierSchema.model_validate(courier_db)
        return courier_schema
    
    async def delete(self, id: int) -> None:
        await validate_courier_exist(id, self.session)

        stmt = delete(CourierTable).where(CourierTable.id == id)
        await self.session.execute(stmt)
        await self.session.commit()
        return None
