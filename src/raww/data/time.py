from datetime import date, time, datetime

from ..views import format_work_time_info


class TimeDelta:
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @property
    def infostr(self) -> str:
        return format_work_time_info(self.hours, self.minutes, self.seconds)
    
    def __add__(self, other):
        self_in_seconds = self.hours*3600 + self.minutes*60 + self.seconds
        other_in_seconds: int = other.hours*3600 + other.minutes*60 + other.seconds
        summa = self_in_seconds + other_in_seconds
        hours = summa // 3600
        summa -= hours*3600
        minutes = summa // 60
        summa -= minutes * 60
        seconds = summa
        return TimeDelta(hours, minutes, seconds)


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
