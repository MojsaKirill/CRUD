import decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from apps.bank.schemas.currency import CurrencyFromDB
from apps.ref.schemas.person import PersonFromDB


class Statuses(str, Enum):
    progress = 'progress'
    accept = 'accept'
    reject = 'reject'


class InvoiceBase(BaseModel):
    person_id: int = Field(..., title='Код персоны')
    currency_id: int = Field(..., title='Код валюты')
    curr_count: decimal.Decimal = Field(..., title='Количество')


class InvoiceView(InvoiceBase):
    id: int = Field(..., title='ID')
    status: Statuses = Field(None, title='Статус')

    class Config:
        orm_mode = True


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    person_id: Optional[int] = Field(None, title='Код персоны')
    currency_id: Optional[int] = Field(None, title='Код валюты')
    curr_count: Optional[decimal.Decimal] = Field(None, title='Количество')
    status: Optional[Statuses] = Field(None, title='Статус')


class InvoiceFromDB(InvoiceBase):
    id: int = Field(..., title='ID')
    person: Optional[PersonFromDB] = Field(None, title='Персона')
    currency: Optional[CurrencyFromDB] = Field(None, title='Валюта')
    status: Statuses = Field(None, title='Статус')

    class Config:
        orm_mode = True
        use_enum_values = True
