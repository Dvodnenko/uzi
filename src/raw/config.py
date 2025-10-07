from pathlib import Path
import json

from .domain import Config, CoreSettings


CONFIG_FILE_PATH = Path.home() / ".config" / "raw" / "config.json"


def load_config() -> Config:
    with open(CONFIG_FILE_PATH, "r") as file:
        data: dict = json.load(file)

    core = CoreSettings(
        data_file="sqlite:///rawdb.sqlite",
        echo=True
    ) # using this url for more convenient testing
    config = Config(core=core)
    return config
