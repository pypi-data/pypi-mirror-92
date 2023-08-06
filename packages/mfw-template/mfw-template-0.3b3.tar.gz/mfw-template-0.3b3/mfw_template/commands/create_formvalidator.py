import os

import click
import yaml
from cookiecutter.main import cookiecutter
from cryptography.fernet import Fernet
from pkg_resources import resource_filename

from ..cli import app, require_config, to_identifier, validate_name


@app.command(help="create a new Form Validator")
@click.option("--name", prompt="Validator Name", callback=validate_name)
@click.pass_context
@require_config
def create_formvalidator(ctx, name):
    conf = ctx.obj["RC"].copy()
    conf["validator_name"] = name
    module_name = to_identifier(name)
    conf["module_name"] = module_name
    cookiecutter(
        resource_filename("mfw_template", "templates/formvalidator"),
        extra_context=conf,
        no_input=True,
        output_dir=conf["project_name"],
        overwrite_if_exists=True,
        skip_if_file_exists=True,
    )
