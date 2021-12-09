from apps.bank.models.currency import Currency
from apps.bank.schemas.currency import CurrencyCreate, CurrencyUpdate
from core.crud import CRUDBase


class CRUDCurrency(CRUDBase[Currency, CurrencyCreate, CurrencyUpdate]):
    pass


currency = CRUDCurrency(Currency)
