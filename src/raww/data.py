import json, os
from pathlib import Path

from .views import ask


DATA_PATH = Path.home() / '.rawdata.json'


# data management

def read_data() -> dict:
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def get_field(data_dict: dict, field: str):
    value = data_dict.get(field)

    return value

def rewrite_data(new_data: dict) -> None:
    with open(DATA_PATH, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)

    return None


# custom methods

def get_tags() -> list:
    data = read_data()
    tags: list = get_field(data, 'tags')

    return tags if tags else []

def get_sessions() -> list[dict]:
    data = read_data()
    sessions: list = get_field(data, 'sessions')

    return sessions if sessions else []

def get_active_session() -> dict:
    data = read_data()
    active_session = get_field(data, 'active_session')

    return active_session if active_session else {}


def update_datafile(tags: list = get_tags(), 
                    active_session: dict = get_active_session(), 
                    sessions: list[dict] = get_sessions()
):
    newdatadict = {
        'tags': tags,
        'active_session': active_session,
        'sessions': sessions
    }
    rewrite_data(newdatadict)

    return None
