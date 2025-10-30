import json

from ..constants import CONFIG_PATH, DEFAULT_CONFIG


def raw_init(force):
    exist = CONFIG_PATH.exists()
    if not exist:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.touch(exist_ok=True)
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        return
    elif force:
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        return
    yield "You already have a non-deafault config file", 1
