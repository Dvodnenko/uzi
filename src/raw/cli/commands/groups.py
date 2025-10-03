import os
import json

import click

from ...domain import Group, Color, EntityType
from ...application import GroupService
from ...infrastructure import PickleDirectoryRepository
from ..config import load_config


@click.command("all")
@click.option("-f", is_flag=True)
@click.pass_context
def groups_all(ctx: click.Context, f):
    repo = PickleDirectoryRepository()
    service = GroupService(repo=repo, config=ctx.obj)
    for group in service.yield_all():
        if f:
            click.echo(ctx.obj.core.rootgroup / group)
            continue
        click.echo(group)


@click.command("print")
@click.option("--fmt")
@click.argument("obj")
@click.option("-c", "-color", is_flag=True)
@click.pass_context
def groups_print(ctx: click.Context, fmt, obj, c):
    if not fmt: fmt = "* {subpath} {icon}"
    repo = PickleDirectoryRepository()
    entity = repo.load(ctx.obj.core.rootgroup / obj)
    if c:
        click.echo(click.style(
            fmt.format(**entity.__dict__),
            fg=entity.color.value
        ))
    else:
        click.echo(fmt.format(**entity.__dict__))


@click.command("create")
@click.argument("path")
@click.option("--icon", default="")
@click.option("--color", 
              type=click.Choice([c.value for c in Color], case_sensitive=False), 
              default=Color.WHITE)
@click.pass_context
def groups_create(ctx: click.Context, path: str, icon: str, color: str):
    picked_color_from_enum = Color._member_map_.get(color.upper(), Color.WHITE)
    service = GroupService(repo=PickleDirectoryRepository(), config=ctx.obj)
    group = Group(path, type=EntityType.GROUP, refs=[], color=picked_color_from_enum, icon=icon)
    ucr = service.create(group=group)
    click.echo(f"raw: {ucr.message}")
    exit(ucr.status_code)


def complete_groups(ctx, param, incomplete):
    config = load_config()
    service = GroupService(repo=PickleDirectoryRepository, config=config)
    return [group for group in service.yield_all() if group.startswith(incomplete)]


@click.command("update")
@click.argument("path", shell_complete=complete_groups)
@click.option("--path", "new_path", default="")
@click.option("--icon", default="")
@click.option("--color", 
              type=click.Choice([c.value for c in Color], case_sensitive=False), 
              default=Color.WHITE)
@click.pass_context
def groups_update(ctx: click.Context, path: str, new_path: str, icon: str, color: str):
    picked_color_from_enum = Color._member_map_.get(color.upper(), Color.WHITE)
    service = GroupService(repo=PickleDirectoryRepository(), config=ctx.obj)
    new_group = Group(subpath=new_path, 
                      type=EntityType.GROUP, 
                      refs=[], 
                      color=picked_color_from_enum, icon=icon)
    ucr = service.update(path, new=new_group)
    click.echo(f"raw: {ucr.message}")
    exit(ucr.status_code)


@click.command("delete")
@click.argument("path", shell_complete=complete_groups)
@click.pass_context
def groups_delete(ctx: click.Context, path: str):
    if os.geteuid() != 0:
        click.echo("raw: This command must be run as root")
        exit(5)
    service = GroupService(repo=PickleDirectoryRepository(), config=ctx.obj)
    ucr = service.delete(path)
    click.echo(f"raw: {ucr.message}")
    exit(ucr.status_code)
