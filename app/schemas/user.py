from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi_users import models


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass













# Базовая модель пользователя
# class UserBase(BaseModel):
#     username: Optional[str] = None
#     email: Optional[EmailStr] = None
#     is_active: Optional[bool] = True
#     is_superuser: bool = False


# class UserCreate(UserBase):
#     username: str
#     email: Optional[EmailStr] = None
#     password: str


# class UserUpdate(UserBase):
#     password: Optional[str] = None


# class UserInDBBase(UserBase):
#     id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# class User(UserInDBBase):
#     pass


# class UserInDB(UserInDBBase):
#     hashed_password: str
