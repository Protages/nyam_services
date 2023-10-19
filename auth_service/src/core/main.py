from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api.api import api_router
from src.core.exception_handlers import install_exception_handlers


app = FastAPI(title='Auth Service')
app.include_router(api_router)

install_exception_handlers(app)


@app.get('/', include_in_schema=False)
async def root():
    # always redirect to /docs page
    return RedirectResponse('/docs')
