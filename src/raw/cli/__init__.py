import click

from .config import load_config

from .commands.groups import groups_create, groups_delete, groups_all, groups_update, groups_print


@click.group()
@click.version_option(package_name="raw")
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()

    if not config.core.rootgroup.exists():
        config.core.rootgroup.mkdir(parents=True, exist_ok=True)

    ctx.obj = config

@raw.group
def groups(): ...

groups.add_command(groups_create, "create")
groups.add_command(groups_update, "update")
groups.add_command(groups_delete, "delete")
groups.add_command(groups_all, "all")
groups.add_command(groups_print, "print")
