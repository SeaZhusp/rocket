from typing import Union

from pydantic import validator, Field

from app.base.schema import RocketBaseSchema
from app.utils.utils import StringUtils


class ProjectCreateBody(RocketBaseSchema):
    name: str = Field(..., title="项目名", description="必传")
    type: int = Field(..., title="项目类型", description="必传")
    description: Union[str, None]

    @validator("name", "type")
    def check_fields(cls, v):
        return StringUtils.not_empty(v)


class ProjectUpdateBody(RocketBaseSchema):
    id: int = Field(..., title="项目id", description="必传")
    name: str = Field(..., title="项目名", description="必传")
    type: int = Field(..., title="项目类型", description="必传")
    description: Union[str, None]
