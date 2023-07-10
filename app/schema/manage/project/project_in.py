from typing import Union

from pydantic import Field

from app.base.schema import RocketBaseSchema


class ProjectCreateBody(RocketBaseSchema):
    name: str = Field(..., title="项目名", description="必传")
    description: Union[str, None]


class ProjectUpdateBody(ProjectCreateBody):
    id: int = Field(..., title="项目id", description="必传")
