from sqlalchemy import Column, Index, Integer, String, Numeric, Date, Identity, SmallInteger
from sqlalchemy.orm import relationship

from db.session import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, Identity(always=True), primary_key=True)
    code = Column(String(length=3), nullable=False)
    scale = Column(SmallInteger, nullable=False, server_default='1')
    rate = Column(Numeric(precision=10, scale=5), nullable=False)
    date_start = Column(Date(), nullable=False)

    invoices = relationship('Invoice', back_populates='currency')


Index('currency_uq01', Currency.code, Currency.date_start, unique=True)
