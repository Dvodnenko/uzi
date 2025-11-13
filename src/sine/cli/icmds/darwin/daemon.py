import subprocess
import os

from ....common.constants import DAEMON_PID_PATH, PLIST_PATH, PLIST_LABEL


def getdpid() -> int | None:
    if DAEMON_PID_PATH.exists():
        with open(DAEMON_PID_PATH, "r") as pidfile:
            return int(pidfile.read())
    return None

def daemon_start(args, flags, kwargs):
    try:
        subprocess.run(["launchctl", "start", PLIST_LABEL], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon started", 0

def daemon_stop(args, flags, kwargs):
    try:
        subprocess.run(["launchctl", "stop", PLIST_LABEL], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon stopped", 0

def daemon_restart(args, flags, kwargs):
    try:
        subprocess.run(["launchctl", "kickstart", "-k", 
                        f"gui/{os.getuid()}/{PLIST_LABEL}"], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon restarted", 0

def daemon_load(args, flags, kwargs):
    try:
        subprocess.run(["launchctl", "bootstrap", 
                        f"gui/{os.getuid()}", PLIST_PATH], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon loaded", 0

def daemon_unload(args, flags, kwargs):
    try:
        subprocess.run(["launchctl", "bootout", 
                        f"gui/{os.getuid()}", PLIST_PATH], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon unloaded", 0

def daemon_remove(args, flags, kwargs):
    try:
        subprocess.run(["launchctl", "remove", PLIST_LABEL], check=True)
    except subprocess.CalledProcessError as e:
        yield f"An error occurred: {e}", 1
        return
    yield "Daemon removed", 0
