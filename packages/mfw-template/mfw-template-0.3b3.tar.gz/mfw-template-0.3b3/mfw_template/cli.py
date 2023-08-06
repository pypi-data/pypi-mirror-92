import os
import sys
from functools import wraps

import click
import importscan
import yaml

import mfw_template


def validate_name(ctx, param, value):
    for c in value:
        if c in ['_']:
            continue
        if not c.isalnum():
            raise click.BadParameter("Name need to be alphanumeric")
    if not value[0].isalpha():
        raise click.BadParameter("Name must start with alphabet")
    return value


def to_identifier(text, lower=True):
    newtxt = ""
    if lower:
        text = text.lower()
    for c in text:
        if c == " ":
            newtxt += "_"
        elif c.isalnum():
            newtxt += c
    return newtxt


def require_config(f):
    def wrapper(ctx, *args, **kwargs):
        if not ctx.obj["RC"]["found_config"]:
            print("Please run this in project directory", file=sys.stderr)
            sys.exit(1)
        return f(ctx, *args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@click.group()
@click.pass_context
def app(ctx=None):
    """Cookiecutter templates for Morp Framework"""
    localrc = os.path.join(os.getcwd(), ".mfwtemplaterc")
    c = {"found_config": False}
    if os.path.exists(localrc):
        with open(localrc, "r") as f:
            c = yaml.load(f, Loader=yaml.Loader)
            c["found_config"] = True

    ctx.ensure_object(dict)
    ctx.obj["RC"] = c


def cli():
    importscan.scan(mfw_template)
    app()
