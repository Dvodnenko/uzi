import pickle
from pathlib import Path

from .session import Session
from .time import TimePoint


class ActiveSession:
    def __init__(
            self, 
            tags: list[str], 
            msg: str,
            start: TimePoint,
            breaks: int
    ):
        self.tags = tags
        self.msg = msg
        self.start = start
        self.breaks = breaks
    @staticmethod
    def _begin(tags: list, msg: str, path: Path): # !underhood method!
        active_session = ActiveSession(tags, msg, TimePoint.now(), 0)
        with open(path, "wb") as file:
            pickle.dump(active_session, file)
        return active_session
    @staticmethod
    def _finish(summary: str, path: Path): # !underhood method!
        with open(path, "rb") as file:
            active_session: ActiveSession = pickle.load(file)
        with open(path, "wb") as file:
            pickle.dump(None, file)
        return Session(
            active_session.tags, 
            active_session.msg,
            summary,
            active_session.start, 
            TimePoint.now(),
            active_session.breaks
        )
