
from app.schemas.codes.user import UserException403Code
from app.exceptions.custom_exception import Custom403Exception

class EmailAlreadyExistsException(Custom403Exception):
    def __init__(self) -> None:
        super().__init__(exception_code=UserException403Code.EMAIL_ALREADY_EXISTS)

class EmailNotFoundException(Custom403Exception):
    def __init__(self) -> None:
        super().__init__(exception_code=UserException403Code.EMAIL_NOT_FOUND)

class InvalidCredentialsException(Custom403Exception):
    def __init__(self) -> None:
        super().__init__(exception_code=UserException403Code.INVALID_CREDENTIALS)

class UserNotFoundException(Custom403Exception):
    def __init__(self) -> None:
        super().__init__(exception_code=UserException403Code.USER_NOT_FOUND)