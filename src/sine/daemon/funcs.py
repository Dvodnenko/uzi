import traceback


def asexc(e: Exception):
    """
    Prints an exception in a pretty way
    """
    
    return " ".join(p for p in traceback.format_exception(e, chain=True))
