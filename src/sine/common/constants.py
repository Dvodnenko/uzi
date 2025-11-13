from pathlib import Path


## Common data

DAEMON_PID_PATH = Path("/tmp/sine.pid")
CONFIG_PATH = Path.home() / ".config" / "sine" / "config.json"
SUPPORTED_SYSTEMS = ("darwin", "linux")
DEFAULT_CONFIG = {
    "core": {
        "db_path": f"{Path.home()}/.sine.sqlite",
    }
}

## Plist file data (for macOS)

PLIST_LABEL = "com.dvodnenko.sine"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_LABEL}.plist"

def generate_plist(script_path: Path | str):

    return {
        "Label": PLIST_LABEL,
        "ProgramArguments": [script_path],
        "KeepAlive": {
            "SuccessfulExit": False,
            "Crashed": True,
        },
        "StandardOutPath": "/tmp/sine.out.log",
        "StandardErrorPath": "/tmp/sine.err.log",
    }


## Service file data (for Linux)

SERVICE_PATH = Path("/etc") / "systemd" / "system" / "sine.service"

def generate_service(script_path: Path | str):
    return f"""
[Unit]
Description=Sine Daemon Service
After=network.target

[Service]
ExecStart={script_path}
Restart=on-failure
RestartSec=3
StandardOutput=append:/tmp/sine.out.log
StandardError=append:/tmp/sine.err.log

SuccessExitStatus=0
RestartPreventExitStatus=0

[Install]
WantedBy=multi-user.target
    """
