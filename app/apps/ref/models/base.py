from sqlalchemy import Column, Integer, DateTime, func, Boolean

from db.session import Base


class RefBase(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    dt_cr = Column(DateTime(timezone=True), server_default=func.sysdate())
    dt_up = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Boolean, default=True)
