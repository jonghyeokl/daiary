from enum import Enum

from app.schemas.codes.enum_mixin import EnumMixin

class Role(EnumMixin, Enum):
    MODEL = 0
    USER = 1