import typing
from dataclasses import dataclass, field

from morpcc.applicationbehavior.base import BaseBehavior

from ..app import App
from .model import {{ cookiecutter.behavior_name }}Model
from .modelui import {{ cookiecutter.behavior_name }}ModelUI


class {{ cookiecutter.behavior_name }}(BaseBehavior):
    """
    Behavior component for {{ cookiecutter.behavior_name }}
    """
    model_marker = {{ cookiecutter.behavior_name }}Model
    modelui_marker = {{ cookiecutter.behavior_name }}ModelUI

    # you may specify entity behavior mapping here , which
    # will mark named entities in this application with 
    # a behavior marker
    # name -> BehaviorClass
    # * -> BehaviorClass (apply to all)
    entity_behavior = {}


@App.application_behavior("{{ cookiecutter.project_name }}.{{ cookiecutter.module_name }}")
def get_behavior(request):
    """Behavior marker factory for {{ cookiecutter.behavior_name }}"""
    return {{ cookiecutter.behavior_name }}


