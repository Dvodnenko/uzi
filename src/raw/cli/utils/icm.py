import sys
from typing import Any, Generator

from ..icmds import (
    daemon_start_darwin, daemon_stop_darwin, raw_init_darwin, daemon_restart_darwin,
    daemon_start_linux, daemon_stop_linux, raw_init_linux, daemon_restart_linux,
    daemon_disable_linux, daemon_enable_linux,
)


if sys.platform.lower() == "darwin":
    INTERNAL_CMD_MAP = {
        "init": raw_init_darwin,
        "daemon": {
            "start": daemon_start_darwin,
            "stop": daemon_stop_darwin,
            "restart": daemon_restart_darwin,
        },
    }
elif sys.platform.lower() == "linux":
    INTERNAL_CMD_MAP = {
        "init": raw_init_linux,
        "daemon": {
            "start": daemon_start_linux,
            "stop": daemon_stop_linux,
            "restart": daemon_restart_linux,
            "enable": daemon_enable_linux,
            "disable": daemon_disable_linux,
        },
    }


def drill(
    branch: dict,
    args: list[str],
    ci: int = 0
):
    next_: Generator[Any, Any, Any] | dict = branch.get(args[ci]) # callback itself or next branch
    if not callable(next_): # then it is not the destination, keep drilling
        return drill(next_, args, ci+1)
    return next_
