import morpfw
import rulez
from datetime import datetime, date
import pytz

from .schema import {{cookiecutter.type_name}}Schema
# {% if cookiecutter.project_type == "morpcc" %}
from .modelui import {{cookiecutter.type_name}}ModelUI, {{cookiecutter.type_name}}CollectionUI
# {% endif %}

class {{cookiecutter.type_name}}Model(morpfw.Model):
    schema = {{cookiecutter.type_name}}Schema

# {% if cookiecutter.project_type == "morpcc" %}
    def ui(self):
        return {{cookiecutter.type_name}}ModelUI(self.request, self,
                self.collection.ui())
# {% endif %}


class {{cookiecutter.type_name}}Collection(morpfw.Collection):
    schema = {{cookiecutter.type_name}}Schema

# {% if cookiecutter.project_type == "morpcc" %}
    def ui(self):
        return {{cookiecutter.type_name}}CollectionUI(self.request, self)
# {% endif %}

