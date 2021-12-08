import datetime
import decimal

from pydantic import BaseModel, Field


class CurrencyBase(BaseModel):
    code: str = Field(..., title='Код', min_length=3, max_length=3)
    rate: decimal.Decimal = Field(..., title='Курс', gt=0)
    date: datetime.date = Field(..., title='Дата')

