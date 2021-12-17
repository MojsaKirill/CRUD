from fastapi import APIRouter

from api.api_v1.endpoints import users, invoices, currencies

router_api_v1 = APIRouter()

router_api_v1.include_router(users.router)
router_api_v1.include_router(invoices.router)
router_api_v1.include_router(currencies.router)
