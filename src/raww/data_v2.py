'''
trying to switch functional aproach to OOP
'''

from pathlib import Path
import pickle


def create_file_if_not_exists(path: Path, default_content):
    if path.exists():
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    with open(path, 'wb') as file:
        pickle.dump(default_content, file)


class Data:

    __ts_df_title = 'tags.pickle'
    
    def __init__(self, dir: Path):
        self.dir = dir

        self.__tags_path = dir / self.__ts_df_title

    @property
    def tags(self):
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
