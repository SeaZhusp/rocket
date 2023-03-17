from app.base.curd import BaseCurd
from app.models.manage.catalog import Catalog


class CatalogFacade(BaseCurd):
    model = Catalog

    @classmethod
    async def list(cls, used, project_id):
        return cls.get_with_params(project_id=project_id, used=used)
