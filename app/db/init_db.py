from faker import Faker

from apps.ref.models.person import Person
from db.base import Base
from db.session import EngineAsync, SessionAsync


async def init_models():
    async with EngineAsync.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def make_fake_data(count: int = 100):
    db = SessionAsync()

    faker = Faker(locale='ru_RU')

    items = []
    for i in range(count):
        if i % 2 == 0:
            ln = faker.last_name_male()
            fn = faker.first_name_male()
            mn = faker.middle_name_male()
        else:
            ln = faker.last_name_female()
            fn = faker.first_name_female()
            mn = faker.middle_name_female()

        pn = faker.unique.random_number(digits=14, fix_len=True)

        items.append(Person(last_name=ln, first_name=fn, middle_name=mn, pers_num=pn))

    db.add_all(items)
    await db.commit()
