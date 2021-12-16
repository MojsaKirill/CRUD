from typing import Any, Optional

from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def __get_first_alpha_upper_dot(item: str = None) -> str:
    result: str = ''
    if isinstance(item, str):
        s = item.strip()
        if len(s) > 0 and s[0].isalpha():
            result = f'{s[0].upper()}.'
    return result


def __get_last_name_title(item: str = None) -> str:
    result: str = ''
    if isinstance(item, str):
        ln = item.strip()
        if len(ln) > 0:
            result = '-'.join([s.title() for s in ln.split('-') if s.isalpha()])
    return result


def get_lfm(last_name: str, first_name: str = None, middle_name: str = None) -> Optional[str]:
    """Из фаМиЛИя иМя ОтчЕство возвращает Фамилия И.О."""
    ln = __get_last_name_title(last_name)
    if ln == '':
        return None

    fn = __get_first_alpha_upper_dot(first_name)
    if fn == '':
        return ln
    else:
        mn = __get_first_alpha_upper_dot(middle_name)

    return f'{ln} {fn}{mn}'


def get_fml(last_name: str, first_name: str = None, middle_name: str = None) -> Optional[str]:
    """Из фаМиЛИя иМя ОтчЕство возвращает И.О. Фамилия"""

    ln = ''
    if isinstance(last_name, str) and len(last_name.strip()) > 0:
        ln = '-'.join([s.strip().title() for s in last_name.strip().split('-') if s.strip().isalpha()])

    if ln == '':
        return None

    fn = __get_first_alpha_upper_dot(first_name)

    if fn == '':
        return ln
    else:
        mn = __get_first_alpha_upper_dot(middle_name)

    return f'{fn}{mn} {ln}'


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def obj_to_dict(obj: Any):
    if isinstance(obj, dict):
        result = obj
    elif isinstance(obj, BaseModel):
        result = obj.dict(exclude_unset=True)
    else:
        result = None
    return result

