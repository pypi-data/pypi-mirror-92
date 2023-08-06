import os
import sys

import click
import yaml
from cookiecutter.main import cookiecutter
from cryptography.fernet import Fernet
from pkg_resources import resource_filename

from ..cli import app, require_config, to_identifier


@app.command(help="create a new resource type")
@click.pass_context
@click.option("--name", prompt="Type Name")
@require_config
def create_resource(ctx, name):
    conf = ctx.obj["RC"].copy()
    conf["type_name"] = name
    proj_name = conf['project_name']
    module_name = to_identifier(name)
    module_name = click.prompt("Module Name", default=module_name)
    type_desc = click.prompt("Type Description", default="%s type" % name)
    api_mount_path = click.prompt("API Mount Path", 
            default="/api/v1/%s.%s" % (proj_name, module_name))
    ui_mount_path = click.prompt("UI Mount Path", 
            default="/%s.%s" % (proj_name, module_name))

    conf.update(
        {
            "module_name": module_name,
            "type_name": name,
            "type_description": type_desc,
            "api_mount_path": api_mount_path,
            "ui_mount_path": ui_mount_path,
        }
    )
    cookiecutter(
        resource_filename("mfw_template", "templates/resource"),
        extra_context=conf,
        no_input=True,
        output_dir=conf["project_name"],
    )
