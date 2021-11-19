# Основной файл проекта
from fastapi import FastAPI
import uvicorn

# from api.api_v1.api import api_router
from apps.auth.routers import user_router
from core.config import settings
from db.session import database

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION,
              openapi_url=f'{settings.API_V1_STR}/openapi.json',
              debug=settings.DEBUG)


@app.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


# app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
