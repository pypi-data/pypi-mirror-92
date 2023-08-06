import morpfw
from morpfw.authz.pas import DefaultAuthzPolicy
from morpfw.crud import permission as crudperm

# {% if cookiecutter.project_type == "morpfw" %}

# {% elif cookiecutter.project_type == "morpcc" %}
import morpcc
import morpcc.permission as ccperm

# {% endif %}

# {% if cookiecutter.project_type == "morpfw" %}


class AppRoot(object):
    """ Application root for {{ cookiecutter.project_name }}"""

    def __init__(self, request):
        self.request = request


class App(DefaultAuthzPolicy, morpfw.SQLApp):
    """ {{ cookiecutter.project_name }} Application """

    pass


@App.path(model=AppRoot, path="/")
def get_approot(request):
    return AppRoot(request)


@App.permission_rule(model=AppRoot, permission=crudperm.All)
def allow_all(identity, context, permission):
    """ Default permission rule, allow all """
    return True


# {% elif cookiecutter.project_type == "morpcc" %}


class AppRoot(morpcc.Root):
    """ Application root for {{ cookiecutter.project_name }}"""

    pass


class App(morpcc.App):
    """ {{ cookiecutter.project_name }} Application """

    pass


@App.path(model=AppRoot, path="/")
def get_approot(request):
    return AppRoot(request)


@App.template_directory()
def get_template_directory():
    return "templates"


# {% endif %}
