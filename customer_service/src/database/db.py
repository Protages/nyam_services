from typing import Any, Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.pool.base import _ConnectionRecord
from sqlite3 import Connection

from src.core.config import settings


class Base(DeclarativeBase):
    pass


if settings.USE_SQLITE:
    async_sqlite_engine = create_async_engine(settings.ASYNC_SQLITE_URL)
    async_sqlite_session_maker = async_sessionmaker(
        async_sqlite_engine, expire_on_commit=False
    )

    async def get_async_session() -> Generator[AsyncSession, Any, None]:
        '''Return async session'''
        async with async_sqlite_session_maker() as session:
            yield session

    @event.listens_for(Engine, 'connect')
    def set_sqlite_pragma(
        dbapi_connection: Connection,
        connection_record: _ConnectionRecord
    ):
        # SQLite by default does not use foreign key constraints unless 
        # you enable them on a per connection basis.
        # https://github.com/sqlalchemy/sqlalchemy/discussions/7974
        # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# sqlite_engine = create_engine(
#     SQLALCHEMY_SQLITE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
