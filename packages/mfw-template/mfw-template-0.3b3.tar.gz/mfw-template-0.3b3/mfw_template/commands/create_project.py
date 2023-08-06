import os
from configparser import ConfigParser

import click
import yaml
from click.decorators import option
from click.termui import prompt
from cookiecutter.main import cookiecutter
from cryptography.fernet import Fernet
from pkg_resources import resource_filename
from datetime import datetime
from ..cli import app, cli, validate_name


def get_git_config():
    gitconfig = os.path.join(os.environ.get("HOME"), ".gitconfig")
    if not os.path.exists(gitconfig):
        return lambda section, option: None
    cf = ConfigParser()
    cf.readfp(open(gitconfig))

    def get_opt(section, option):
        if cf.has_option(section, option):
            return cf.get(section, option)
        return None

    return get_opt


git_conf = get_git_config()


@app.command(help="create a new MorpFW project")
@click.option("--name", prompt="Project Name", callback=validate_name)
@click.option(
    "--type",
    type=click.Choice(["morpcc", "morpfw"], case_sensitive=False),
    prompt="Project Type",
)
@click.option("--url", prompt="Project URL", default="http://myproject.github.io")
@click.option(
    "--author", prompt="Author Name", default=git_conf("user", "name"), required=True
)
@click.option(
    "--author-email",
    prompt="Author Email",
    default=git_conf("user", "email"),
    required=True,
)
@click.option(
    "--license",
    type=click.Choice(["Apache2", "GPLv3+", "AGPLv3+", "Proprietary"], case_sensitive=False),
    prompt="License",
)
def create_project(name, type, url, author, author_email, license):
    now = datetime.now()
    rpm_date = now.strftime('%a %b %d %Y')
    cookiecutter(
        resource_filename("mfw_template", "templates/project"),
        extra_context={
            "project_name": name,
            "project_type": type,
            "project_url": url,
            "project_license": license,
            "author_name": author,
            "author_email": author_email,
            "fernet_key": Fernet.generate_key().decode("utf-8"),
            "rpm_date": rpm_date,
        },
        no_input=True,
    )
