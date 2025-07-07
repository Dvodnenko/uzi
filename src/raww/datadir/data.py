import pickle
from pathlib import Path

from .active_session import ActiveSession
from .session import Session
from ..views import create_file_if_not_exists


class Data:

    __ts_df_title = 'tags.pickle'
    __ss_df_title = 'sessions.pickle'
    __as_df_title = 'active_session.pickle'
    
    def __init__(self, dir: Path):
        self.dir = dir

        self.__tags_path = dir / self.__ts_df_title
        self.__sessions_path = dir / self.__ss_df_title
        self.__as_path = self.dir / self.__as_df_title
    def begin_session(self, tags: list[str]) -> ActiveSession:
        return ActiveSession._begin(tags, path=self.__as_path)
    def finish_session(self) -> Session:
        active_session = ActiveSession._finish(self.__as_path)
        self.sessions = [*self.sessions, active_session]
        return active_session

    @property
    def tags(self) -> list[str]:
        create_file_if_not_exists(self.__tags_path, [])

        with open(self.__tags_path, 'rb') as file:
            tags: list[str] = pickle.load(file)
        return tags
    @tags.setter
    def tags(self, newtags):
        create_file_if_not_exists(self.__tags_path, [])

        with open(self.__tags_path, 'wb') as file:
            pickle.dump(newtags, file)
        return None

    @property
    def sessions(self) -> list[Session]:
        create_file_if_not_exists(self.__sessions_path, [])

        with open(self.__sessions_path, 'rb') as file:
            sessions: list[str] = pickle.load(file)
        return sessions
    @sessions.setter
    def sessions(self, newsessions):
        create_file_if_not_exists(self.__sessions_path, [])

        with open(self.__sessions_path, 'wb') as file:
            pickle.dump(newsessions, file)
        return None

    @property
    def active_session(self) -> ActiveSession | None:
        create_file_if_not_exists(self.__as_path, None)

        with open(self.__as_path, 'rb') as file:
            active_session: ActiveSession | None = pickle.load(file)
        return active_session
    @active_session.setter
    def active_session(self, activesession):
        create_file_if_not_exists(self.__as_path, None)

        with open(self.__as_path, 'wb') as file:
            pickle.dump(activesession, file)
        return None
