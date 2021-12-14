import decimal
from typing import Optional, Any

from email_validator import validate_email
from pydantic import BaseModel, Field, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


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


class UserView(BaseModel):
    id: int = Field(..., title='ID')
    username: str = Field(..., title='Имя пользователя')

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    balance: Optional[decimal.Decimal] = Field(0, title='Баланс')
    banker: Optional[bool] = Field(False, title='Признак банкира')


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, title='Пароль')


class UserFromDB(UserBase):
    id: int = Field(..., title='ID')
    username: str = Field(..., title='Имя пользователя')
    email: Optional[str] = Field(None, title='Адрес e-mail')
    balance: decimal.Decimal = Field(..., title='Баланс')
    banker: bool = Field(..., title='Признак банкира')

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
