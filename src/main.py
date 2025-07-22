import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from api import router as api_router
from core.config import settings
from core.dependencies.helper import db_helper

from fastapi import FastAPI

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    async with AsyncTron(
        AsyncHTTPProvider(api_key=settings.trongrid.api_key)
    ) as tron_client:
        app.state.tron_client = tron_client
        yield
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
