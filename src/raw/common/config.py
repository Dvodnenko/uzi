from pathlib import Path
import json


CONFIG_FILE_PATH = Path.home() / ".config" / "raw" / "config.json"


def load_config() -> dict:
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            data: dict = json.load(file)

        return data
    except FileNotFoundError as e:
        return {}
