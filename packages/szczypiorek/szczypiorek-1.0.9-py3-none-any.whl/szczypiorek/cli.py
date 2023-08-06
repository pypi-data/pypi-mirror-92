
from glob import glob
import os
import re
import importlib
import json

import click

from .utils import load_yaml
from .git import assert_is_git_ignored
from .exceptions import BaseException
from . import crypto


@click.group()
def cli():
    """Expose multiple commands allowing one to work with szczypiorek."""
    pass


@click.command()
@click.argument('env_path')
def print_env(env_path):
    """Print currently loaded env variables into stdout."""

    def hide_sensitive(name, value):
        if (name.endswith('password') or
                name.endswith('key') or
                name.endswith('secret')):
            return 10 * '*'

        return value

    env_path_parts = env_path.split('.')
    env_path = '.'.join(env_path_parts[:-1])
    env_variable = env_path_parts[-1]
    env = getattr(importlib.import_module(env_path), env_variable)
    for k, v in env.env.items():
        v = hide_sensitive(k, v)

        try:
            if isinstance(json.loads(v), dict):
                v = json.loads(v)
                for kk, vv in v.items():
                    v[kk] = hide_sensitive(kk, vv)

                v = json.dumps(v, indent=4)

        except (json.decoder.JSONDecodeError, TypeError):
            pass

        click.echo(f'{k}: {v}')


@click.command()
@click.argument('path')
@click.option('--key_filepath', '-k')
def encrypt(path, key_filepath=None):
    """Encrypt all yml files in a given path."""

    if os.path.isdir(path):
        filepaths = sorted(
            glob(os.path.join(path, '*.yml')) +
            glob(os.path.join(path, '*.yaml')))

    else:
        filepaths = [path]

    for filepath in filepaths:
        with open(filepath, 'r') as f:
            szczyp_filepath = re.sub(
                r'(\.yml|\.yaml)', '.szczyp', filepath)

            click.secho(f'[ENCRYPTING] {filepath}', color='green')

            try:
                assert_is_git_ignored(filepath)

                content = f.read()
                # -- used here only to validate
                load_yaml(content)
                content = crypto.encrypt(content, key_filepath)

            except BaseException as e:
                raise click.ClickException(e.args[0])

            # -- WRITE at the end when it's certain that all went well
            with open(szczyp_filepath, 'w') as g:
                g.write(content)


@click.command()
@click.argument('path')
@click.option('--key_filepath', '-k')
def decrypt(path, key_filepath=None):
    if os.path.isdir(path):
        filepaths = glob(os.path.join(path, '*.szczyp'))

    else:
        filepaths = [path]

    for filepath in filepaths:
        with open(filepath, 'r') as f:
            yml_filepath = filepath.replace('.szczyp', '.yml')
            click.secho(f'[DECRYPTING] {filepath}', color='green')

            try:
                content = crypto.decrypt(f.read(), key_filepath)

            except BaseException as e:
                raise click.ClickException(e.args[0])

            # -- WRITE at the end when it's certain that all went well
            with open(yml_filepath, 'w') as g:
                g.write(content)


cli.add_command(encrypt)
cli.add_command(decrypt)
cli.add_command(print_env)
