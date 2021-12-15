import decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Statuses(str, Enum):
    progress = 'progress'
    accept = 'accept'
    reject = 'reject'


class InvoiceBase(BaseModel):
    user_id: int = Field(..., title='Код пользователя')
    currency_id: int = Field(..., title='Код валюты')
    curr_count: decimal.Decimal = Field(..., title='Количество')


class InvoiceView(InvoiceBase):
    id: int = Field(..., title='ID')
    status: Statuses = Field(..., title='Статус')

    class Config:
        orm_mode = True
        use_enum_values = True


class InvoiceCreate(BaseModel):
    currency_id: int = Field(..., title='Код валюты')
    curr_count: decimal.Decimal = Field(..., title='Количество', gt=0)


class InvoiceUpdate(InvoiceBase):
    user_id: Optional[int] = Field(None, title='Код пользователя')
    currency_id: Optional[int] = Field(None, title='Код валюты')
    curr_count: Optional[decimal.Decimal] = Field(None, title='Количество')
    status: Optional[Statuses] = Field(None, title='Статус')


# class InvoiceFromDB(InvoiceBase):
#     id: int = Field(..., title='ID')
#     person: Optional[PersonFromDB] = Field(None, title='Персона')
#     currency: Optional[CurrencyView] = Field(None, title='Валюта')
#     status: Statuses = Field(None, title='Статус')
#
#     class Config:
#         orm_mode = True
#         use_enum_values = True
