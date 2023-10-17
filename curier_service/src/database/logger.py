import time
import logging

from sqlalchemy import event
from sqlalchemy.engine.base import Connection
from sqlalchemy.dialects.sqlite.base import SQLiteExecutionContext
from sqlite3 import Cursor

from src.database.db import async_sqlite_engine


logging.basicConfig()

logger = logging.getLogger(' QueryLogger')
logger.setLevel(logging.INFO)


@event.listens_for(async_sqlite_engine.sync_engine, 'before_cursor_execute')
def before_db_query_logger(
    conn: Connection,
    cursor: Cursor,
    statement: str,
    parameters: tuple,
    context: SQLiteExecutionContext,
    executemany: bool
) -> None:
    conn.info.setdefault('query_start_time', []).append(time.time())
    p = ', '.join(str(p) for p in parameters)
    line = f'\n{"="*80}'
    msg = f'{p}{line}\n{statement}\n'
    logger.info(' ' + msg)


@event.listens_for(async_sqlite_engine.sync_engine, 'after_cursor_execute')
def after_db_query_logger(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    line = f'\n{"="*80}'
    msg = f'Total Time: {total}{line}'
    logger.info(' ' + msg)
