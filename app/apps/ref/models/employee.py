from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tab_num = Column(Integer, unique=True, nullable=False)
    person_id = Column(Integer,
                       ForeignKey('persons.id', ondelete='SET NULL', name=f'{__tablename__}_fk01'),
                       nullable=True)

    # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html
    person = relationship('Person', back_populates='employees',
                          lazy='joined',
                          innerjoin=False)


employees = Employee.__table__
