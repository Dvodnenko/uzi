from importlib.metadata import version

import click

from .tags import tag
from .sessions import begin_session, finish_session, pause_session, check_sessions


@click.command('version')
def show_version():
    v = version('raww')

    click.echo(f'🦇 raww v{v}')


@click.group()
def raw():
    ...


## commands ##

# std 
raw.add_command(show_version)

# tags
raw.add_command(tag)

# sessions
raw.add_command(check_sessions, name='sessions')
raw.add_command(begin_session, name='begin')
raw.add_command(begin_session, name='start')
raw.add_command(finish_session, name='finish')
raw.add_command(finish_session, name='stop')
raw.add_command(pause_session, name='pause')
