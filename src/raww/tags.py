import click

from .data import get_tags, update_datafile


@click.command('tags')
@click.option('--new')
@click.pass_context
def tag(
    ctx: click.Context,
    new: str
):

    raww_datafile = ctx.obj['raww_datafile']
    mytags = get_tags(raww_datafile)

    if new:
        if new in mytags:
            click.echo(f'🦇 tag {new} already exists')
            exit(1)
        else:
            update_datafile(raww_datafile, tags=[*mytags, new])
            click.echo(f'🦇 new tag - {new}')
            exit(0)
    else:
        if mytags == []:
            click.echo('🦇 your tag list is empty right now')
            exit(1)
        for tag in mytags:
            click.echo(f'* {tag}')
