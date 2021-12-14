# Основной файл проекта
import logging
# import os
# import sys
# import warnings

from fastapi import FastAPI
import uvicorn

from api.api_v1.api import api_router
from api.api_v1.endpoints.oauth import auth_router

from core.config import init_logging, settings


# os.environ['SQLALCHEMY_WARN_20'] = 'True'
# if not sys.warnoptions:
#     warnings.simplefilter("default")

logger = init_logging(__name__)

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION,
              openapi_url=f'{settings.API_V1_STR}/openapi.json',
              debug=settings.DEBUG)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(auth_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
