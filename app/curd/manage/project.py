from sqlalchemy.sql.elements import and_

from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.manage.project import Project


class ProjectDao(BaseCurd):
    model = Project

    @classmethod
    async def create(cls, project):
        ant = cls.get_with_existed(name=project.name)
        if ant:
            raise BusinessException("项目已存在")
        o = Project(**project.dict())
        return cls.insert_with_model(model_obj=o)

    @classmethod
    async def list(cls, page: int = 1, limit: int = 10, search: str = None):
        total, projects = cls.get_with_pagination(page=page, limit=limit, _sort=["create_time"],
                                                  name=f"%{search}%" if search else None)
        # total, projects = cls.get_with_join(page=page, limit=limit, query_fields=[User.fullname],
        #                                     join_con=[User, User.id == Project.owner])
        return total, projects

    @classmethod
    async def delete(cls, pk):
        return cls.delete_with_id(pk=pk)

    @classmethod
    async def update(cls, project):
        filter_list = [and_(cls.model.name == project.name, cls.model.id != project.id)]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("项目已存在")
        return cls.update_with_id(model=project)

    @classmethod
    async def list_all(cls):
        return cls.get_with_params(_sort=["create_time"])

    @classmethod
    async def exist_by_id(cls, pk):
        return cls.get_with_existed(filter_list=[cls.model.id == pk])
