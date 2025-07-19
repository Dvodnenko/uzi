from pathlib import Path

import click

from .config import load_config, save_config, CONFIG_FILE, DEFAULT_RAW_DIR
from .tags import tag
from .sessions import begin_session, finish_session, pause_session, check_sessions


@click.group()
@click.version_option(package_name="raw")
@click.pass_context
def raw(ctx: click.Context):
    config = load_config()
    raw_directory = Path(config.get("raw_directory", str(DEFAULT_RAW_DIR)))

    if not raw_directory.exists():
        raw_directory.mkdir(parents=True, exist_ok=True)

    ctx.obj = {"raw_directory": raw_directory, "config": config}

@raw.group()
def config():
    ...

@config.command()
def create():
    config = load_config()
    save_config(config)
    click.echo("🦇 configuration created")

@config.command()
def show():
    if not CONFIG_FILE.exists():
        click.echo("🦇 no configuration found")
        exit(1)
    
    config = load_config()
    click.echo(f"raw data directory: {config.get("raw_directory", DEFAULT_RAW_DIR)}")

@config.command()
@click.option("-n", "--new-directory", type=click.Path(exists=False), help="")
def update(new_directory: str):
    config = load_config()
    config["raw_directory"] = new_directory

    save_config(config)
    click.echo(f"raw data directory set to '{new_directory}'")


## commands ##

# tags
raw.add_command(tag)

# sessions
raw.add_command(check_sessions, name="sessions")
raw.add_command(begin_session, name="begin")
raw.add_command(begin_session, name="start")
raw.add_command(finish_session, name="finish")
raw.add_command(finish_session, name="stop")
raw.add_command(pause_session, name="pause")
