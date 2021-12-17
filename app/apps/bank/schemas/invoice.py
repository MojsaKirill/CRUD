import datetime
import decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from apps.auth.schema import UserViewJoin
from apps.bank.schemas.currency import CurrencyViewJoin


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
    inv_date: datetime.date = Field(..., title='Дата заявки')
    status: Statuses = Field(..., title='Статус')

    class Config:
        orm_mode = True
        use_enum_values = True


class InvoiceViewFull(BaseModel):
    id: int = Field(..., title='ID')
    # user_id: int = Field(..., title='Код пользователя')
    user: UserViewJoin = Field(..., title='Пользователь')
    # currency_id: int = Field(..., title='Код валюты')
    currency: CurrencyViewJoin = Field(..., title='Валюта')
    curr_count: decimal.Decimal = Field(..., title='Количество')
    inv_date: datetime.date = Field(..., title='Дата заявки')
    status: Statuses = Field(..., title='Статус')

    class Config:
        orm_mode = True
        use_enum_values = True


class InvoiceCreate(BaseModel):
    curr_code: str = Field(..., title='Код валюты', min_length=3, max_length=3)
    curr_count: decimal.Decimal = Field(..., title='Количество')
    inv_date: datetime.date = Field(..., title='Дата заявки')


class InvoiceUpdate(InvoiceBase):
    status: Optional[Statuses] = Field(None, title='Статус')
