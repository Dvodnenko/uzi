import json
from typing import Generator, Any

from .services.folders import FolderService
from .services.sessions import SessionService
from .services.tags import TagService
from .services.tasks import TaskService
from .repositories.folder import saFolderRepository
from .repositories.session import saSessionRepository
from .repositories.tag import saTagRepository
from .repositories.task import saTaskRepository
from .database.session import Session


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
    data: dict = json.loads(request)

    args = data["args"]
    kwargs = data["kwargs"]
    flags = data["flags"]

    orm_session = Session()
    repository_instance = REPOSITORIES.get(args[0])(orm_session)
    service_instance = SERVICES.get(args[0])(repository_instance)
    if not service_instance:
        yield format_response_json(f"Service not found: {args[0]}", 1)
        return
    if not hasattr(service_instance, args[1]):
        yield format_response_json(f"Method not found: {args[0]}.{args[1]}", 1)
        return
    method: Generator[tuple[str, int], Any, None] = getattr(service_instance, args[1])

    try:
        for row, status_code in method(args=args[2:],flags=flags,**kwargs):
            yield format_response_json(row, status_code)

    except Exception as e:
        method.close()
        raise e
    finally:
        orm_session.expunge_all()
        orm_session.close()
        return
