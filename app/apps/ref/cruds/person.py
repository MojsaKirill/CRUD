from apps.ref.models.person import Person
from apps.ref.schemas.person import PersonCreate, PersonUpdate
from core.crud import CRUDBase


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    pass


person = CRUDPerson(Person)
