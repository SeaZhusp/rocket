from pydantic import BaseModel
from app.core.Constants import ERROR_MSG_TEMPLATES


class RocketBaseBody(BaseModel):
    # 入参基础模型
    class Config:
        error_msg_templates = ERROR_MSG_TEMPLATES
