from typing import Union

from pydantic import Field

from app.base.schema import RocketBaseSchema


class CatalogCreateBody(RocketBaseSchema):
    name: str = Field(..., title="目录名", description="必传")
    parent_id: Union[int, None]
    project_id: int = Field(..., title="项目id", description="必传")


class CatalogUpdateBody(CatalogCreateBody):
    id: int = Field(..., title="目录id", description="必传")
