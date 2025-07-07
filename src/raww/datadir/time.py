from datetime import date, time, datetime

from src.raww.views import format_work_time_info


class TotalWorkTime:
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @property
    def infostr(self) -> str:
        return format_work_time_info(self.hours, self.minutes, self.seconds)


class TimePoint:

    def __init__(self, date: date, time: time): 
        self.date = date
        self.time = time

    @staticmethod
    def now():
        now = datetime.now()
        return TimePoint(now.date(), now.time())
    
    @property
    def datetime(self):
        return datetime(
            self.date.year, self.date.month, self.date.day,
            self.time.hour, self.time.minute, self.time.second
        )
