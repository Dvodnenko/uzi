from .time import TotalWorkTime, TimePoint


class Session:
    def __init__(
            self, 
            tags: list[str], 
            start: TimePoint, 
            end: TimePoint, 
            breaks: int = 0
    ):
        self.tags = tags
        self.start = start
        self.end = end
        self.breaks = breaks

    @property
    def total(self):
        diff = (self.end.datetime - self.start.datetime).seconds - self.breaks

        hours = diff // 3600
        diff -= hours*3600
        minutes = diff // 60
        diff -= minutes * 60
        seconds = diff

        return TotalWorkTime(hours=hours, minutes=minutes, seconds=seconds)
