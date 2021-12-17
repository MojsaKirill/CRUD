import enum

from sqlalchemy import Column, Date, Integer, ForeignKey, Enum, Numeric, Identity, func
from sqlalchemy.orm import relationship

from db.session import Base


class Statuses(str, enum.Enum):
    progress = 'progress'
    accept = 'accept'
    reject = 'reject'


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, Identity(always=True), primary_key=True)
    inv_date = Column(Date(), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id', ondelete='RESTRICT'), nullable=False)
    curr_count = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
    status = Column(Enum(Statuses, create_constraint=True, name='statuses'), nullable=False,
                    default=Statuses.progress)

    user = relationship('User', back_populates='invoices', lazy='joined', innerjoin=False)
    currency = relationship('Currency', back_populates='invoices', lazy='joined', innerjoin=False)
