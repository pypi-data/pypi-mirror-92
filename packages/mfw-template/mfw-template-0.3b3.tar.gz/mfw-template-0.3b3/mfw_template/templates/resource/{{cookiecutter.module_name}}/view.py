import rulez

from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm

from ..app import App
from .model import {{cookiecutter.type_name}}Model, {{cookiecutter.type_name}}Collection
# {% if cookiecutter.project_type == "morpcc" %}
from .modelui import {{cookiecutter.type_name}}ModelUI, {{cookiecutter.type_name}}CollectionUI
# {% endif %}


