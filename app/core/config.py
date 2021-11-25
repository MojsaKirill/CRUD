# Конфигурация проекта
from pydantic import BaseSettings
from starlette.config import Config

config = Config('.env')


class Settings(BaseSettings):
    DEBUG: bool = config('DEBUG', cast=bool, default=True)
    FUTURE: bool = config('FUTURE', cast=bool, default=True)   # Use 2.0 SQLAlchemy style
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = config('SECRET_KEY', cast=str,
                             default='FaOsibHOugjgCdQDAaC6Apnblx9m6aF6FPgHqAA/3WnSKDftsf2I99dAA5LEfFG5qJCVe3aqkXLyJ3pZ')
    PROJECT_NAME: str = config('PROJECT_NAME', cast=str,
                               default='CRUD Project')
    PROJECT_VERSION: str = config('PROJECT_VERSION', cast=str,
                                  default='0.0.1')
    SQLALCHEMY_DATABASE_URL: str = config('SQLALCHEMY_DATABASE_URL', cast=str,
                                          # default='sqlite+pysqlite:///./crud.db')
                                          default='sqlite+aiosqlite:///./crud.db')
    FIRST_SUPERUSER_NAME: str = config('FIRST_SUPERUSER_NAME', cast=str,
                                       default='admin')
    FIRST_SUPERUSER_EMAIL: str = config('FIRST_SUPERUSER_EMAIL', cast=str,
                                        default='admin@example.com')
    FIRST_SUPERUSER_PASSWORD: str = config('FIRST_SUPERUSER_PASSWORD', cast=str,
                                           default='123456')


settings = Settings()
