import json
from pathlib import Path


# data management

def read_data(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def rewrite_data(path: Path, new_data: dict) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)

    return None


# custom methods

def get_tags(path: Path) -> list:
    data = read_data(path)
    tags: list = data.get('tags', [])

    return tags

def get_sessions(path: Path) -> list[dict]:
    data = read_data(path)
    sessions: list = data.get('sessions', [])

    return sessions

def get_active_session(path: Path) -> dict:
    data = read_data(path)
    active_session = data.get('active_session', {})

    return active_session


def update_datafile(
        path: Path,
        tags: list = None, 
        active_session: dict = None, 
        sessions: list[dict] = None
):

    tags = get_tags(path) if tags == None else tags
    active_session = get_active_session(path) if active_session == None else active_session
    sessions = get_sessions(path) if sessions == None else sessions

    newdatadict = {
        'tags': tags,
        'active_session': active_session,
        'sessions': sessions
    }
    rewrite_data(path, newdatadict)

    return None
