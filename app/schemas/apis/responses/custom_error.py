from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.exceptions.custom_exception import CustomException


class CustomErrorExample:
    def __init__(
        self,
        exception: CustomException,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.exception = exception
        self.title = exception.__class__.__name__ if not title else title
        self.description = exception.code.to_str() if not description else description


class CustomErrorResponse(BaseModel):
    examples: List[CustomErrorExample]

    def to_openapi(self) -> Dict[str, Any]:
        return {
            "content": {
                "application/json": {
                    "examples": {
                        example.title: {
                            "description": example.description,
                            "value": {
                                "code": example.exception.code.value,
                                "msg": example.exception.code.to_str(),
                                "detail": example.exception.detail,
                            },
                        }
                        for example in self.examples
                    },
                },
            }
        }

    class Config:
        arbitrary_types_allowed = True
