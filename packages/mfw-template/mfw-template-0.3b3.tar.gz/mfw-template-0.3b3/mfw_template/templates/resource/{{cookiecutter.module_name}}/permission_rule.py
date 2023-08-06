from morpfw.crud import permission as crudperm
from ..app import App
from .model import {{cookiecutter.type_name}}Model, {{cookiecutter.type_name}}Collection
from .modelui import {{cookiecutter.type_name}}ModelUI, {{cookiecutter.type_name}}CollectionUI


@App.permission_rule(model={{cookiecutter.type_name}}Collection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model={{cookiecutter.type_name}}Model,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

