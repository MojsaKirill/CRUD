from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED

from apps.auth.crud import get_user_auth

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'FaOsibHOugjgCdQDAaC6Apnblx9m6aF6FPgHqAA/3WnSKDftsf2I99dAA5LEfFG5qJCVe3aqkXLyJ3pZ'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_security = HTTPBasic()


# def get_current_username(credentials: HTTPBasicCredentials = Depends(auth_security)):
#     if not (credentials.username == 'foo' and credentials.password == 'pass'):
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
#                             detail='Incorrect username or password',
#                             headers={"WWW-Authenticate": "Basic"})
#     return credentials.username


async def get_current_user(credentials: HTTPBasicCredentials = Depends(auth_security)):
    user = await get_user_auth(credentials.username, credentials.password)

    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={"WWW-Authenticate": "Basic"})
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
