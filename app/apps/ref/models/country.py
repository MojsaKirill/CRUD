from sqlalchemy import Column, String, Integer, DateTime, Boolean, func

from db.session import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_cnt = Column(String(length=100))
    dt_cr = Column(DateTime(timezone=True), default=func.sysdate())
    dt_up = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Boolean, default=True)

