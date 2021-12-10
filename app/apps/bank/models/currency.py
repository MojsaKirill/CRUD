from sqlalchemy import Column, DateTime, Index, Integer, String, Numeric, Date, UniqueConstraint
from sqlalchemy.orm import relationship

from db.session import Base


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(length=3), nullable=False)
    rate = Column(Numeric(precision=10, scale=5), nullable=False)
    date_start = Column(Date(), nullable=False)

    invoices = relationship('Invoice', back_populates='currency')

    # __table_args__ = (Index('currency_uq01', 'code', 'date', unique=True),)


Index('currency_uq01', Currency.code, Currency.date_start, unique=True)
