import subprocess

from ...constants import DAEMON_PID_PATH, SERVICE_PATH


def getdpid() -> int | None:
    if DAEMON_PID_PATH.exists():
        with open(DAEMON_PID_PATH, "r") as pidfile:
            return int(pidfile.read())
    return None

def daemon_start(args, kwargs, flags):
    try:
        subprocess.run(["sudo", "systemctl", "start", SERVICE_PATH], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon started", 0

def daemon_enable(args, kwargs, flags):
    try:
        subprocess.run(["sudo", "systemctl", "enable", SERVICE_PATH], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon enabled", 0

def daemon_disable(args, kwargs, flags):
    try:
        subprocess.run(["sudo", "systemctl", "disable", SERVICE_PATH], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon disabled", 0

def daemon_stop(args, kwargs, flags):
    try:
        subprocess.run(["systemctl", "stop", SERVICE_PATH], check=True)
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
