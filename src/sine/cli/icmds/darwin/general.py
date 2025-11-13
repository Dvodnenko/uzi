import shutil
import json
import plistlib

from ....common.constants import CONFIG_PATH, DEFAULT_CONFIG, generate_plist, PLIST_PATH
from ....common.config import load_config


def init(args, flags, kwargs):
    
    ## Config

    force = "F" in flags

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.touch(exist_ok=True)
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
    elif force:
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
    else:
        yield "You already have a non-default config file", 1
        

    ## Plist file (for macOS)

    config = load_config()
    plist_content = generate_plist(config.get("daemon_bin_path", 
                                              shutil.which("cos")))
    if not PLIST_PATH.exists():
        PLIST_PATH.touch(exist_ok=True)
        with open(PLIST_PATH, "wb") as file:
            plistlib.dump(plist_content, file)
        return
    elif force:
        with open(PLIST_PATH, "wb") as file:
            plistlib.dump(plist_content, file)
        return
    else:
        yield "You already have a non-default plist file", 1
