from app.core.exc.exceptions import BusinessException
from app.base.curd import BaseCrud
from app.models.system.project import Project


class ProjectDao(BaseCrud):
    model = Project

    @classmethod
    async def create(cls, project):
        filter_list = [cls.model.name == project.username]
        ant = cls.get_with_existed(filter_list=filter_list)
        if ant:
            raise BusinessException("项目已存在")
        project = Project(project)
        return cls.insert_by_model(model_obj=project)
