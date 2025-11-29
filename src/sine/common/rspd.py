from .parsers import parse_afk, parse_sql


def generate_rspd(argv: list[str]):
    
    rspd = {
        "source": argv,
        "ps": {
            "afk": parse_afk(argv),
            "sql": parse_sql(argv),
        }
    }

    return rspd
