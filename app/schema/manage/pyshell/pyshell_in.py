from app.base.schema import RocketBaseSchema


class DebugFunctionBody(RocketBaseSchema):
    module_name: str
    func_express: str


class CreatePyshellBody(RocketBaseSchema):
    module_name: str


class SavePyshellBody(CreatePyshellBody):
    code: str
