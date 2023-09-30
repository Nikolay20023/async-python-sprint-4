from fastapi import FastAPI
import uvicorn
from fastapi.responses import ORJSONResponse

from api.v1 import base
from core.config import AppSettings
from core import config


setting = AppSettings()


app = FastAPI(
    title=setting.app_title,
    redoc_url=None,
    default_response_class=ORJSONResponse,
    openapi_url='/api/openapi.json'
)


app.include_router(base.router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT
    )
