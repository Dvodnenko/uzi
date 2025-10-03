from pathlib import Path
import pickle

from ...domain import EntityRepository, Entity, Group


class PickleFileRepository(EntityRepository):
    """
    Files repository `.pickle` implementation

    Used to work with `FileEntities`, such as Sessions, Tags etc.
    """

    ext: str | None = "pickle"

    def dump(self, path: Path, entity: Entity):
        with open(f"{path}", "wb") as file:
            pickle.dump(entity, file)
        return None

    def load(self, path: Path) -> Entity:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data
    
    # current & new - NOT subpaths, but absolute paths. starting from config rootgroup
    def mv(self, current: Path, new: Path, *, rootgroup):
        current.rename(new)
        return None


class PickleDirectoryRepository(EntityRepository):
    """
    Directories repository `.pickle` implementation
    """

    ext: str | None = "pickle"
    __file_repo = PickleFileRepository()

    def dump(self, path: Path, entity: Group):
        self.__file_repo.dump(path, entity)
        return None

    def load(self, path: Path) -> Entity: # path example: IT/Work
        data = self.__file_repo.load(path / f".self")
        return data
    
    # current & new - NOT subpaths, but absolute paths, starting from config rootgroup
    def mv(self, current: Path, new: Path, *, rootgroup: Path):
        current.rename(new)
        self_path = new / f".self"
        data = self.__file_repo.load(self_path)
        data.subpath = new.relative_to(rootgroup)
        self.__file_repo.dump(new / ".self", data)
        return None
