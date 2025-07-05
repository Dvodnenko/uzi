import json
from pathlib import Path


DATA_PATH = Path.home() / '.rawdata.json'


# data management

def read_data() -> dict:
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def rewrite_data(new_data: dict) -> None:
    with open(DATA_PATH, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)

    return None


# custom methods

def get_tags() -> list:
    data = read_data()
    tags: list = data.get('tags', [])

    return tags

def get_sessions() -> list[dict]:
    data = read_data()
    sessions: list = data.get('sessions', [])

    return sessions

def get_active_session() -> dict:
    data = read_data()
    active_session = data.get('active_session', {})

    return active_session


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
