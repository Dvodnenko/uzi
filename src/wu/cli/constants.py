from pathlib import Path


## Common data

DAEMON_PID_PATH = Path("/tmp/wu.pid")
CONFIG_PATH = Path.home() / ".config" / "wu" / "config.json"
SUPPORTED_SYSTEMS = ("darwin", "linux")
DEFAULT_CONFIG = {
    "data_file_path": f"{Path.home()}/.wu.sqlite",

    "formats": {
        "folder": "* #{id} \u001b[{color}m{title}\u001b[0m",
        "tag": "* #{id} \u001b[{color}m{title}\u001b[0m",
        "task": "* #{id} \u001b[{color}m{title}\u001b[0m [{status}] {description}",

        "session": "#{id} {title}\n{sw}, {sm} {sd} {sy} {sH}:{sM}:{sS} - {eH}:{eM}:{eS} \u001b[42m {total} \u001b[0m\n\t{links}\n\n\t{description}\n\t{summary}",
    }
}

## Plist file data (for macOS)

PLIST_LABEL = "com.dvodnenko.wu"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_LABEL}.plist"

def generate_plist(script_path: Path | str):

    return {
        "Label": PLIST_LABEL,
        "ProgramArguments": [script_path],
        "KeepAlive": {
            "SuccessfulExit": False,
            "Crashed": True,
        },
        "StandardOutPath": "/tmp/wu.out.log",
        "StandardErrorPath": "/tmp/wu.err.log",
    }


## Service file data (for Linux)

SERVICE_PATH = Path("/etc") / "systemd" / "system" / "wu.service"

def generate_service(script_path: Path | str):
    return f"""
[Unit]
Description=Wu Daemon Service
After=network.target

[Service]
ExecStart={script_path}
Restart=on-failure
RestartSec=3
StandardOutput=append:/tmp/wu.out.log
StandardError=append:/tmp/wu.err.log

SuccessExitStatus=0
RestartPreventExitStatus=0

[Install]
WantedBy=multi-user.target
    """
