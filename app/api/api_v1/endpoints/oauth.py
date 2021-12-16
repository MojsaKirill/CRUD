import uuid

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from apps.auth.crud import get_user_by_name, check_username_or_email, create_user, get_user_by_email
from apps.auth.schema import UserCreate, UserView, UserForgotPassword
from core.exceptions import login_invalid_exception, ProjectException
from core.security import create_access_token, get_current_user, get_token_user
from core.utils import verify_password

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=UserView, summary='Регистрация')
async def auth_register(user: UserCreate):
    result = await check_username_or_email(user.username, user.email)
    if not result:
        result = await create_user(user)
    return result


@router.post('/login', summary='Авторизация')
async def auth_login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_name(credentials.username)
    if not user:
        raise login_invalid_exception
    if not verify_password(credentials.password, user.password):
        raise login_invalid_exception
    access_token = create_access_token(data={'sub': credentials.username})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_info': {
            'email': user.email,
        }
    }


# @router.get('/logout', summary='Завершение сеанса')
# async def auth_logout(token: str = Depends(get_token_user),
#                       user: UserView = Depends(get_current_user)):
#     return token


# @router.post('/forgot-password', summary='Восстановление пароля')
# async def auth_forgot_password(request: UserForgotPassword):
#     result = await get_user_by_email(request.email)
#     if not result:
#         raise ProjectException(status_code=404, detail='This e-mail not exist.')
#     reset_code = str(uuid.uuid1())
#     return reset_code

