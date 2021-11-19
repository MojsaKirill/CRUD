from fastapi import APIRouter

from apps.auth.managers import fastapi_users, jwt_authentication

user_router = APIRouter()

user_router.include_router(fastapi_users.get_auth_router(jwt_authentication),
                           prefix="/auth/jwt", tags=["auth"],)

user_router.include_router(fastapi_users.get_register_router(),
                           prefix="/auth", tags=["auth"],)

# user_router.include_router(fastapi_users.get_reset_password_router(),
#                            prefix="/auth",
#                            tags=["auth"],)

# user_router.include_router(fastapi_users.get_verify_router(),
#                            prefix="/auth",
#                            tags=["auth"],)

user_router.include_router(fastapi_users.get_users_router(),
                           prefix="/users",
                           tags=["users"],)
