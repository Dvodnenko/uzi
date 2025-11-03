import subprocess
import os

from ...constants import DAEMON_PID_PATH, PLIST_PATH


def getdpid() -> int | None:
    if DAEMON_PID_PATH.exists():
        with open(DAEMON_PID_PATH, "r") as pidfile:
            return int(pidfile.read())
    return None

def daemon_start(args, kwargs, flags):
    try:
        subprocess.run(["launchctl", "bootstrap", 
                        f"gui/{os.getuid()}", PLIST_PATH], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon started", 0

def daemon_stop(args, kwargs, flags):
    try:
        subprocess.run(["launchctl", "bootout", 
                        f"gui/{os.getuid()}", PLIST_PATH], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon stopped", 0

def daemon_restart(args, kwargs, flags):
    try:
        yield from daemon_stop(args, kwargs, flags)
        yield from daemon_start(args, kwargs, flags)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon restarted", 0
