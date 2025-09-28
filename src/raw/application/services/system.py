from ...domain import Session, Config, EntityRepository


class SystemService:
    def __init__(self, repo: EntityRepository, config: Config):
        self.repo = repo
        self.config = config
        self.system_path = self.config.core.raw_path / ".system"

    def get_active_session(self) -> Session | None:
        _system_as_path = self.system_path / f"active_session.{self.repo.ext}"
        as_ = self.repo.load(_system_as_path)
        return as_
    
    def set_active_session(self, data: Session | None) -> None:
        self.repo.dump(self.system_path, data)
        return None
