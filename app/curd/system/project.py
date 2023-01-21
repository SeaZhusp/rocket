from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCurd
from app.models.system.project import Project
from app.models.system.user import User


class ProjectDao(BaseCurd):
    model = Project

    @classmethod
    async def create(cls, project):
        filter_list = [cls.model.name == project.name]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("项目已存在")
        project = Project(project)
        return cls.insert_with_model(model_obj=project)

    @classmethod
    async def query_with_name(cls, page: int = 1, limit: int = 10, search: str = None):
        # total, projects = cls.get_with_pagination(page=page, limit=limit, _sort=['create_time'],
        #                                           name=f"%{search}%" if search else None)
        total, projects = cls.get_with_join(page=page, limit=limit, query_fields=[User.fullname],
                                            join_con=[User, User.id == Project.owner])
        return total, projects
