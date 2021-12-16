import decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Statuses(str, Enum):
    progress = 'progress'
    accept = 'accept'
    reject = 'reject'


class InvoiceBase(BaseModel):
    currency_id: int = Field(..., title='Код валюты')
    curr_count: decimal.Decimal = Field(..., title='Количество')


class InvoiceView(InvoiceBase):
    id: int = Field(..., title='ID')
    user_id: int = Field(..., title='Код пользователя')
    status: Statuses = Field(..., title='Статус')

    class Config:
        orm_mode = True
        use_enum_values = True


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    status: Optional[Statuses] = Field(None, title='Статус')
