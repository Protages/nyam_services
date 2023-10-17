from src.services.courier import CourierService
from src.repositories.courier.sqlalchemy import CourierSQLAlchemyRepo


def courier_service() -> CourierService:
    return CourierService(CourierSQLAlchemyRepo)
