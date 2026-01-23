from enum import Enum

from app.schemas.codes.enum_mixin import EnumMixin

class ChatManner(EnumMixin, Enum):
    FRIENDLY = 1
    POLITE = 2
    COOL = 3

class DiaryFont(EnumMixin, Enum):
    DEFAULT = 1
    HANDWRITING = 2