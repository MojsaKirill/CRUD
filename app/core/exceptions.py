from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},)

invoice_change_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Invoice cannot be changed',)


login_invalid_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Incorrect username or password',)


class DuplicatedEntryError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=422, detail=message)


class DBOperationError(HTTPException):
    def __init__(self, e: Exception):
        super().__init__(status_code=422, detail=e.statement)
