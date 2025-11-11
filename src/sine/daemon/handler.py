import json

from .services.base import Service
from .services.folders import FolderService
from .services.sessions import SessionService
from .services.tags import TagService
from .services.tasks import TaskService
from .repositories.folder import saFolderRepository
from .repositories.session import saSessionRepository
from .repositories.tag import saTagRepository
from .repositories.task import saTaskRepository
from .database.session import Session
from .funcs import asexc


SERVICES = {
    "folders": FolderService,
    "sessions": SessionService,
    "tags": TagService,
    "tasks": TaskService,
}

REPOSITORIES = {
    "folders": saFolderRepository,
    "sessions": saSessionRepository,
    "tags": saTagRepository,
    "tasks": saTaskRepository,
}


def format_response_json(
    message: str,
    status_code: int
) -> str:
    return json.dumps({
        "message": message,
        "status_code": status_code
    }) + "\n"


def handlecmd(request: str):
    argv: list = json.loads(request)

    orm_session = Session()
    repository_instance = REPOSITORIES.get(argv[0])(orm_session)
    service_instance: Service = SERVICES.get(argv[0])(repository_instance)
    if not service_instance:
        yield format_response_json(f"Service not found: {argv[0]}", 1)
        return
    
    method = service_instance.execute(argv[1:])

    try:
        for row, status_code in method:
            yield format_response_json(row, status_code)

    except Exception as e:
        method.close()
        yield format_response_json(asexc(e), 1)
    finally:
        orm_session.expunge_all()
        orm_session.close()
        return
