import json

from .services.folders import FolderService


SERVICES = {
    "folders": FolderService
}


def handlecmd(request: str):
    data: dict = json.loads(request)

    args = data["args"]
    kwargs = data["kwargs"]
    flags = data["flags"]
    
    service_instance = SERVICES[args[0]]()
    method = service_instance.__getattribute__(args[1])
    
    response = method(
        args=args[2:],
        flags=flags,
        **kwargs
    )

    return response.message
