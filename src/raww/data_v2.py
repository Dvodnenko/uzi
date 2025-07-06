'''
trying to switch functional aproach to OOP
'''

from pathlib import Path
import pickle

from .views import format_work_time_info


def create_file_if_not_exists(path: Path, default_content):
    if path.exists():
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    with open(path, 'wb') as file:
        pickle.dump(default_content, file)


class TotalWorkTime:
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @property
    def infostr(self) -> str:
        return format_work_time_info(self.hours, self.minutes, self.seconds)


worktime = TotalWorkTime(hours=0, minutes=0, seconds=0)
print(worktime.infostr)


class Data:

    __ts_df_title = 'tags.pickle'
    
    def __init__(self, dir: Path):
        self.dir = dir

        self.__tags_path = dir / self.__ts_df_title

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


DIR_PATH = Path.home() / 'Dev' / 'raww' / 'src' / 'tests' # test path

data = Data(DIR_PATH)
