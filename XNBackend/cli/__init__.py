# -*- encoding: utf-8 -*-
# import os

# import click
# from flask.cli import FlaskGroup
# from XNBackend.app.factory import create_app


# @click.group(cls=FlaskGroup, create_app=create_app)
# @click.option(
#     '--settings', help='specify a settings file. it overrides XN_SETTINGS environ',
#     type=click.Path(exists=True, dir_okay=False, resolve_path=True)
# )
# def cli(settings=None):
#     """Management script for the XNBackend application"""
#     if settings:
#         click.echo('using settings file %s' % (settings, ))
#         os.environ['XN_SETTINGS'] = settings


# from . import user

from .user import user_cli
from .systemd import systemd
