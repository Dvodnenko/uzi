from pathlib import Path


DAEMON_PID_PATH = Path("/tmp/raw.pid")
CONFIG_PATH = Path.home() / ".config" / "raw" / "config.json"
SUPPORTED_SYSTEMS = ("darwin", "linux")
DEFAULT_CONFIG = {
    "data_file_path": f"sqlite:///{Path.home()}/.raw.sqlite",

    "formats": {
        "folder": "* \u001b[{color}m{title}\u001b[0m\n",
        "tag": "* \u001b[{color}m{title}\u001b[0m\n",

        "session": "{title}\n{sw}, {sm} {sd} {sy} {sH}:{sM}:{sS} - {eH}:{eM}:{eS} \u001b[42m {total} \u001b[0m\n\t{links}\n\n\t{description}\n\t{summary}",
    }
}
