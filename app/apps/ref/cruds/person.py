from typing import Any, Dict, List, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_, select

from apps.ref.models.person import Person
from apps.ref.schemas.person import PersonCreate, PersonUpdate
from core.crud import CRUDBase
from core.utils import get_fml, get_lfm


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):

    async def get_list(self, *args, skip: int = 0, limit: int = 100) -> List[Person]:
        sql = select(self.model).offset(skip).limit(limit)
        if isinstance(*args, str):
            sql = sql.where(or_(Person.pers_num.like(f'%{args[0]}%'),
                                Person.last_name.like(f'%{args[0]}%')))
        async with self.db.obtain_session() as sess:
            rows = await sess.execute(sql)
        results = rows.scalars().all()
        return results

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
