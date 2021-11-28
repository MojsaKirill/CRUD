from faker import Faker

from apps.ref.models.person import Person
from db.base import Base
from db.session import EngineAsync, SessionAsync


async def init_models():
    async with EngineAsync.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def make_fake_data():
    db = SessionAsync()

    faker = Faker(locale='ru_RU')

    items = []
    for i in range(150):
        if i % 2 == 0:
            l = faker.last_name_male()
            f = faker.first_name_male()
            m = faker.middle_name_male()
        else:
            l = faker.last_name_female()
            f = faker.first_name_female()
            m = faker.middle_name_female()

        n = faker.unique.random_number(digits=14, fix_len=True)

        items.append(Person(last_name=l, first_name=f, middle_name=m, pers_num=n))

    db.add_all(items)
    await db.commit()
