from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tab_num = Column(Integer, unique=True, nullable=False)
    person_id = Column(Integer, ForeignKey('person.id', ondelete='SET NULL'), nullable=True)

    # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html
    person = relationship('Person', back_populates='employees', lazy='joined', innerjoin=False)


employees = Employee.__table__
