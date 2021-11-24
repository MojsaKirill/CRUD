from fastapi import APIRouter

from api.api_v1.endpoints import home, users, persons, employees

api_router = APIRouter()
api_router.include_router(home.router, tags=['home'])
# api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(persons.router, prefix='/persons', tags=['persons'])
api_router.include_router(employees.router, prefix='/employees', tags=['employees'])
