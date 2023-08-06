from morpfw.static import StaticRoot as BaseStaticRoot
from .app import App


class StaticRoot(BaseStaticRoot):

    module = '{{ cookiecutter.project_name }}'
    directory = 'static_files'


@App.path(model=StaticRoot, path='/__static__/{{ cookiecutter.project_name }}', absorb=True)
def get_staticroot(absorb):
    return StaticRoot(absorb)

