from datetime import datetime

from pydantic import BaseModel


class RocketBaseDto(BaseModel):
    id: int
    create_time: datetime
    update_time: datetime
    deleted: int

    # 返参基础模型
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
