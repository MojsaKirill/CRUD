from fastapi import APIRouter

from api.api_v1.endpoints import home, oauth, persons, employees, currencies, invoices, users

api_router = APIRouter()
api_router.include_router(home.router, tags=['Home'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(currencies.router, prefix='/currencies', tags=['Currencies'])
api_router.include_router(invoices.router, prefix='/invoices', tags=['Invoices'])

# api_router.include_router(oauth.router, tags=['Auth'])
# api_router.include_router(persons.router, prefix='/persons', tags=['persons'])
# api_router.include_router(employees.router, prefix='/employees', tags=['employees'])
