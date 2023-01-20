from typing import Union

from pydantic import validator, Field

from app.base.schema import RocketBaseBody
from app.utils.utils import StringUtils


class ProjectCreateBody(RocketBaseBody):
    name: str = Field(..., title="项目名", description="必传")
    type: int = Field(..., title="项目类型", description="必传")
    description: Union[str, None]
    owner: int = Field(..., title="项目所有者", description="必传")

    @validator('name', 'type', 'owner')
    def check_fields(cls, v):
        return StringUtils.not_empty(v)


class ProjectUpdateBody(ProjectCreateBody):
    id: int = Field(..., title="用户id", description="必传")
