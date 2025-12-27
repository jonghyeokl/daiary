from enum import Enum

# 모든 에러 Enum은 이 클래스를 상속한다.


class ExceptionCodeBase(Enum):
    pass

    def to_str(self) -> str:
        raise NotImplementedError


class Exception400CodeBase(ExceptionCodeBase):
    pass

    def to_str(self) -> str:
        raise NotImplementedError


class Exception403CodeBase(ExceptionCodeBase):
    pass

    def to_str(self) -> str:
        raise NotImplementedError


class Exception404CodeBase(ExceptionCodeBase):
    pass

    def to_str(self) -> str:
        raise NotImplementedError


class Exception409CodeBase(ExceptionCodeBase):
    pass

    def to_str(self) -> str:
        raise NotImplementedError
