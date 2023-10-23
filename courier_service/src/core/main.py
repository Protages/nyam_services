from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

# from src.database.db import Base, sqlite_engine
from src.api.http.api import api_router
from src.core.exception_handlers import install_exception_handlers
from src.core.config import settings


if settings.QUERY_LOGGER:
    # need to import a logger for it to work
    from src.database.logger import logger  # noqa: F401


app = FastAPI(title='Restaurant Service')
app.include_router(api_router)

install_exception_handlers(app)


@app.get('/', include_in_schema=False)
async def root():
    # always redirect to /docs page
    return RedirectResponse('/docs')
