import os

import click
import yaml
from cookiecutter.main import cookiecutter
from cryptography.fernet import Fernet
from pkg_resources import resource_filename

from ..cli import app, require_config, to_identifier, validate_name


@app.command(help="create a new Entity Behavior")
@click.pass_context
@click.option("--name", prompt="Behavior Name", callback=validate_name)
@require_config
def create_behavior(ctx, name):
    conf = ctx.obj["RC"].copy()
    conf["behavior_name"] = name
    module_name = to_identifier(name)
    module_name = click.prompt("Module Name", default=module_name)
    conf["module_name"] = module_name
    cookiecutter(
        resource_filename("mfw_template", "templates/behavior"),
        extra_context=conf,
        no_input=True,
        output_dir=conf["project_name"],
    )
