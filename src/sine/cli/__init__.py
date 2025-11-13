import sys

import halo

from .utils.resolve import resolve_callback
from ..common.constants import SUPPORTED_SYSTEMS
from ..common import parse_afk


def execute(callback, is_internal, argv):

    spinner = halo.Halo(text="Loading...", spinner="dots", color="white", 
                        stream=sys.stderr)
    spinner.start()

    if is_internal:
        argv = parse_afk(argv) # all internal callbacks use AKF parsing strategy
    for i in callback(*argv):
        spinner.clear()
        yield i


def sin():

    argv = sys.argv[1:]

    try:
        if not argv:
            exit(0)

        if not sys.platform.lower() in SUPPORTED_SYSTEMS:
            print(f"Unsupported operating system: {sys.platform}")
            exit(1)

        callback, is_internal = resolve_callback(argv)

        error_ocurred: int = 0

        for response in execute(callback, is_internal, argv):
            print(response[0])
            if response[1] != 0: error_ocurred = 1

        exit(error_ocurred)
    except KeyboardInterrupt:
        print("Cancelled by user")
        exit(0)
