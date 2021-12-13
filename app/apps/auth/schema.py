import decimal
from typing import Optional, Any

from email_validator import validate_email
from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    username: str = Field(..., title='Имя пользователя')
    email: Optional[str] = Field(None, title='Адрес e-mail')
    balance: decimal.Decimal = Field(..., title='Баланс')
    banker: bool = Field(..., title='Признак банкира')

    @validator('email')
    def _validate_email(cls, v: Any) -> Optional[str]:
        if v:
            if not validate_email(v):
                raise ValueError('E-mail invalid')
        return v


class UserView(UserBase):
    id: int = Field(..., title='ID')

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, title='Пароль')
