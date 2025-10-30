import os
import signal

from ..constants import DAEMON_PID_PATH


def getdpid() -> int | None:
    if DAEMON_PID_PATH.exists():
        with open(DAEMON_PID_PATH, "r") as pidfile:
            return int(pidfile.read())
    return None


def daemon_start(args, kwargs, flags):
    from raw.rawd.daemon import main
    main()
    exit(0)


def daemon_stop(args, kwargs, flags):
    dpid = getdpid()
    if not dpid:
        yield "Daemon is not started", 1
        return
    os.kill(dpid, signal.SIGTERM)
    yield f"Daemon stopped", 0
