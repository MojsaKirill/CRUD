# Основной файл проекта
from fastapi import FastAPI
import uvicorn

from api.api_v1.api import api_router
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION,
              openapi_url=f'{settings.API_V1_STR}/openapi.json',
              debug=settings.DEBUG)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
