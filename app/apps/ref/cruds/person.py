from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from apps.ref.models.person import Person
from apps.ref.schemas.person import PersonCreate, PersonUpdate
from core.crud import CRUDBase
from core.utils import get_fml, get_lfm


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):

    async def update(self, *, obj_db: Person,
                     obj_in: Union[PersonUpdate, Dict[str, Any]]) -> Person:
        obj_data = jsonable_encoder(obj_db)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data['name_lfm'] = get_lfm(update_data.get('last_name') or obj_data['last_name'],
                                          update_data.get('first_name') or obj_data['first_name'],
                                          update_data.get('middle_name') or obj_data['middle_name'])
        update_data['name_fml'] = get_fml(update_data.get('last_name') or obj_data['last_name'],
                                          update_data.get('first_name') or obj_data['first_name'],
                                          update_data.get('middle_name') or obj_data['middle_name'])
        return await super().update(obj_db=obj_db, obj_in=update_data)


person = CRUDPerson(Person)
