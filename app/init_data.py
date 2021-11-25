import asyncio

from db.init_db import init_models


def db_init_models() -> None:
    asyncio.run(init_models())
    print('DB init')


def main() -> None:
    db_init_models()


if __name__ == '__main__':
    main()
