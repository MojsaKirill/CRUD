import asyncio

from db.init_db import init_models, make_fake_data


def db_init_models() -> None:
    # asyncio.run(init_models())
    # print('DB init')
    asyncio.run(make_fake_data())


def main() -> None:
    db_init_models()


if __name__ == '__main__':
    main()
