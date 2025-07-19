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
    
    def __sub__(self, other):
        """
        most likely ``self`` is the ``end`` time; ``other`` - the `start` one.
        because you do "``end - start``" (like in math) to get delta (here, timedelta)
        """

        self_date = self.date
        self_time = self.time
        self_datetime = datetime(
            self_date.year, self_date.month, self_date.day,
            self_time.hour, self_time.minute, self_time.second
        )
        other_date = other.date
        other_time = other.time
        other_datetime = datetime(
            other_date.year, other_date.month, other_date.day,
            other_time.hour, other_time.minute, other_time.second
        )

        diff = (other_datetime - self_datetime)
        hours = diff // 3600
        diff -= hours*3600
        minutes = diff // 60
        diff -= minutes * 60
        seconds = diff

        return TimeDelta(hours=hours, minutes=minutes, seconds=seconds)
