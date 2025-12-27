import orjson

from typing import Any


def orjson_serializer(obj: Any) -> str:
    return orjson.dumps(
        obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC
    ).decode()
