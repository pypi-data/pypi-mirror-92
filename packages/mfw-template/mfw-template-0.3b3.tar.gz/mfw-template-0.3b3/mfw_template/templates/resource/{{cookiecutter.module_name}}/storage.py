import morpfw
import morpfw.sql
from morpfw.sql import construct_orm_model
import sqlalchemy as sa
import sqlalchemy_utils as sautils
import sqlalchemy_jsonfield as sajson

from ..app import App
from .model import {{cookiecutter.type_name}}Model

class {{cookiecutter.type_name}}Storage(morpfw.SQLStorage):

    model = {{cookiecutter.type_name}}Model

    orm_model = construct_orm_model(
            schema={{cookiecutter.type_name}}Model.schema,
            metadata=morpfw.sql.Base.metadata,
            name='{{cookiecutter.project_name}}_{{cookiecutter.module_name}}'
    )

@App.storage(model={{cookiecutter.type_name}}Model)
def get_storage(model, request, blobstorage):
    return {{cookiecutter.type_name}}Storage(request, blobstorage=blobstorage)


@App.blobstorage(model={{cookiecutter.type_name}}Model)
def get_blobstorage(model, request):
    return request.app.get_config_blobstorage(request)
