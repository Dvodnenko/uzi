import click

from .data import Data


@click.command('tags')
@click.option('--new')
@click.pass_context
def tag(
    ctx: click.Context,
    new: str
):

    raww_directory = ctx.obj['raww_directory']
    data = Data(raww_directory)
    mytags = data.tags

    if new:
        if new in mytags:
            click.echo(f'🦇 tag {new} already exists')
            exit(1)
        else:
            data.tags = [*data.tags, new]
            click.echo(f'🦇 new tag - {new}')
            exit(0)
    else:
        if mytags == []:
            click.echo('🦇 your tag list is empty right now')
            exit(1)
        for tag in mytags:
            click.echo(f'* {tag}')
