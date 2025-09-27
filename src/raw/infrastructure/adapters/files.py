from pathlib import Path
import pickle

from ...domain import EntityRepository, Entity


class PickleFileRepository(EntityRepository):
    """
    Files repository `.pickle` implementation

    Used to work with `FileEntities`, such as Sessions, Tags etc.
    """

    ext: str | None = ".pickle"

    def dump(self, basepath: Path, entity: Entity):
        _path = basepath / f"{entity.subpath}.{self.ext}"
        with open(_path, "rb") as file:
            pickle.dump(entity, file)
        return None

    def load(self, path: Path) -> Entity:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data


class PickleGroupRepository(EntityRepository):
    """
    Groups repository `.pickle` implementation
    """

    ext: str | None = ".pickle"

    def dump(self, basepath: Path, entity: Entity):
        group_path = basepath / f"{entity.subpath}"
        self_path = group_path / f".self.{self.ext}"
        with open(self_path, "rb") as file:
            pickle.dump(entity, file)
        return None

    def load(self, path: Path) -> Entity:
        with open(path/f".self.{self.ext}", "rb") as file:
            data = pickle.load(file)
        return data
