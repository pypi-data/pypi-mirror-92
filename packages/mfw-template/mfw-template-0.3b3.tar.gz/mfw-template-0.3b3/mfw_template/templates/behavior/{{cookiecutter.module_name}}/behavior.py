import typing
from dataclasses import dataclass, field

from morpcc.behavior.base import BaseBehavior

from ..app import App
from .model import ({{ cookiecutter.behavior_name }}Collection,
                    {{ cookiecutter.behavior_name }}Model)
from .modelui import ({{ cookiecutter.behavior_name }}CollectionUI,
                      {{ cookiecutter.behavior_name }}ModelUI)
from .schema import {{ cookiecutter.behavior_name }}Schema


class {{ cookiecutter.behavior_name }}(BaseBehavior):
    """ Behavior component for {{ cookiecutter.behavior_name }}"""
    schema = {{ cookiecutter.behavior_name }}Schema
    model_marker = {{ cookiecutter.behavior_name }}Model
    modelui_marker = {{ cookiecutter.behavior_name }}ModelUI
    collection_marker = {{ cookiecutter.behavior_name }}Collection
    collectionui_marker = {{ cookiecutter.behavior_name }}CollectionUI


@App.behavior('{{ cookiecutter.project_name }}.{{ cookiecutter.module_name }}')
def get_behavior(request):
    """ Behavior factory for {{ cookiecutter.behavior_name }} """
    return {{ cookiecutter.behavior_name }}
