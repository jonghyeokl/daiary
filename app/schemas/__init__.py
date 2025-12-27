from pydantic import BaseModel


class HealthInfoResponse(BaseModel):
    project_name: str
