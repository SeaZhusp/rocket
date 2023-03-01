from app.base.dto import RocketBaseDto


class ApiDto(RocketBaseDto):
    name: str
    level: str
    status: int
    desc: str
    service: str
    method: str
    path: str
    project_id: int
    catalog_id: int
    env_id: int
    create_user: str
    update_user: str
