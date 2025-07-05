import click

from .tags import tag
from .sessions import begin_session, finish_session, pause_session, check_sessions


@click.group()
@click.version_option(package_name='raww')
def raw():
    ...


## commands ##

# tags
raw.add_command(tag)

# sessions
raw.add_command(check_sessions, name='sessions')
raw.add_command(begin_session, name='begin')
raw.add_command(begin_session, name='start')
raw.add_command(finish_session, name='finish')
raw.add_command(finish_session, name='stop')
raw.add_command(pause_session, name='pause')
