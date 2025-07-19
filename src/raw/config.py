import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "raw"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_RAW_DIR = Path.home() / ".raw"


def load_config():
    if not CONFIG_FILE.exists():
        return {"raw_directory": str(DEFAULT_RAW_DIR)}
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)
    
def save_config(config: dict): 
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
