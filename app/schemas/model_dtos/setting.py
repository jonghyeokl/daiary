from datetime import datetime

from pydantic import BaseModel

from app.db.models.setting.setting import Setting

class SettingModelDTO(BaseModel):
    setting_id: str
    user_id: str
    chat_manner: int
    diary_font: int
    created_dt: datetime
    updated_dt: datetime

    @classmethod
    def from_model(cls, model: Setting) -> "SettingModelDTO":
        return cls(
            setting_id=str(model.setting_id),
            user_id=str(model.user_id),
            chat_manner=model.chat_manner,
            diary_font=model.diary_font,
            created_dt=model.created_dt,
            updated_dt=model.updated_dt,
        )