# Основной файл проекта
import logging
# import os
# import sys
# import warnings

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.api_v1.api import api_router
from api.api_v1.endpoints import oauth

from core.config import init_logging, settings


# os.environ['SQLALCHEMY_WARN_20'] = 'True'
# if not sys.warnoptions:
#     warnings.simplefilter("default")
from core.exceptions import ProjectException

logger = init_logging(__name__)

app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              version=settings.PROJECT_VERSION,
              openapi_url=f'{settings.API_V1_STR}/openapi.json',
              debug=settings.DEBUG)

app.include_router(oauth.router)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


@app.exception_handler(ProjectException)
async def unicorn_exception_handler(request: Request, exc: ProjectException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'code': exc.status_code,
            'message': exc.detail
        },
        headers=exc.headers,
    )


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
