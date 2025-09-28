from datetime import datetime

from ...domain import Session, EntityRepository, Config, UseCaseResponse
from .system import SystemService


class SessionService:
    def __init__(self, repo: EntityRepository, config: Config):
        self.repo = repo
        self.config = config
        self.ending = "-SESSION"
    
    def begin(self, session: Session) -> UseCaseResponse[Session]:
        system_service = SystemService(repo=self.repo, config=self.config)
        as_ = system_service.get_active_session()
        if as_:
            return UseCaseResponse(message="Session already started", status_code=3, data=as_)
        system_service.set_active_session(data=session)
        (self.config.core.raw_path / session.subpath / \
            f"{session.title}{self.ending}.{self.repo.ext}").touch()
        self.repo.dump(self.config.core.raw_path, session)
        return UseCaseResponse(
            message=f"Session started", data=session
        )
    
    def finish(self) -> UseCaseResponse[Session]:
        system_service = SystemService(repo=self.repo, config=self.config)
        as_ = system_service.get_active_session()
        if not as_:
            return UseCaseResponse(message="No active Session", status_code=4, data=as_)
        system_service.set_active_session(None)
        as_.end = datetime.now()
        self.repo.dump(self.config.core.raw_path, as_)
        return UseCaseResponse(message="Session finished", data=as_)
    
    def update(self, subpath: str, new: Session) -> UseCaseResponse[Session]:
        current_path = self.config.core.raw_path / f"{subpath}{self.ending}.{self.repo.ext}"
        if not current_path.exists() or not current_path.is_file():
            return UseCaseResponse(
                message=f"Session not found: {subpath}", status_code=4
            )
        new_path = self.config.core.raw_path / new.subpath / f"{new.title}{self.ending}.{self.repo.ext}"
        if new_path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Session already exists: {new.subpath}/{new.title}", 
            )
        self.repo.mv(current_path, new_path)
        self.repo.dump(new)
        return UseCaseResponse(
            message=f"Session updated: {subpath}", data=new
        )
    
    def delete(self, subpath: str) -> UseCaseResponse[Session]:
        _path = self.config.core.raw_path / f"{subpath}{self.ending}.{self.repo.ext}"
        if not _path.exists() or not _path.is_file():
            return UseCaseResponse(
                message=f"Session not found: {subpath}", status_code=4
            )
        _path.unlink()
        return UseCaseResponse(
            message=f"Session deleted: {subpath}"
        )
