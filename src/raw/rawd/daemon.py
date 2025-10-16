import daemon
import socket
import os
import sys
import signal
from daemon import pidfile
import atexit

import setproctitle

from .handler import handlecmd
from .database.orm_registry import mapping_registry
from .database.session import engine
from .database.mappings import map_tables


SOCKET_PATH = "/tmp/raw.sock"
PID_PATH = "/tmp/raw.pid"


def cleanup():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    if os.path.exists(PID_PATH):
        os.remove(PID_PATH)


def run():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)

    atexit.register(cleanup)

    mapping_registry.metadata.create_all(bind=engine)
    map_tables()

    try:
        while True:
            conn, _ = server.accept()
            request = conn.recv(1024).decode()
            if not request:
                conn.close()
                continue
            
            response = handlecmd(request)
            conn.sendall(response.encode())
            conn.close()
    finally:
        server.close()
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)


def main():
    context = daemon.DaemonContext(
        working_directory="/tmp",
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(PID_PATH),
        stdout=open("/tmp/raw.out", "w+"),
        stderr=open("/tmp/raw.err", "w+"),
        detach_process=True,
    )

    setproctitle.setproctitle("rawd")

    context.signal_map = {
        signal.SIGTERM: lambda signum, frame: sys.exit(0),
        signal.SIGINT: lambda signum, frame: sys.exit(0)
    }

    with context:
        run()


if __name__ == "__main__":
    main()
