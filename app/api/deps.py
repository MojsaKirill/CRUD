from typing import Generator

from starlette.requests import Request

from db.session import SessionLocal


# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


def get_db(request: Request):
    return request.state.db
