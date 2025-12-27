import asyncio
import traceback
from typing import Any
from typing import Dict
from typing import Optional

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.schemas.codes.exception_code_base import Exception400CodeBase
from app.schemas.codes.exception_code_base import Exception403CodeBase
from app.schemas.codes.exception_code_base import Exception404CodeBase
from app.schemas.codes.exception_code_base import Exception409CodeBase
from app.schemas.codes.exception_code_base import ExceptionCodeBase


class CustomException(Exception):
    def __init__(
        self,
        response_code: int,
        exception_code: ExceptionCodeBase,
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.response_code = response_code
        self.code = exception_code
        self.detail = detail


class Custom400Exception(CustomException):
    def __init__(
        self,
        exception_code: Exception400CodeBase,
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            response_code=400,
            exception_code=exception_code,
            detail=detail,
        )


class Custom403Exception(CustomException):
    def __init__(
        self,
        exception_code: Exception403CodeBase,
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            response_code=403,
            exception_code=exception_code,
            detail=detail,
        )


class Custom404Exception(CustomException):
    def __init__(
        self,
        exception_code: Exception404CodeBase,
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            response_code=404,
            exception_code=exception_code,
            detail=detail,
        )


class Custom409Exception(CustomException):
    def __init__(
        self,
        exception_code: Exception409CodeBase,
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            response_code=409,
            exception_code=exception_code,
            detail=detail,
        )


class CustomExceptionResponse(BaseModel):
    code: int
    msg: str
    detail: Optional[Dict[str, Any]]

