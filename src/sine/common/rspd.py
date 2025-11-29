from .parsers import parse_afk


def generate_rspd(argv: list[str]):
    
    rspd = {
        "source": argv,
        "ps": {
            "afk": parse_afk(argv),
        }
    }

    return rspd
