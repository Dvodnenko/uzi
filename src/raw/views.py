from pathlib import Path
import pickle


def format_work_time_info(
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0
) -> str:

    if hours == 0 and minutes == 0 and seconds == 0:
        return "0s"
    
    work_time_info = ""

    if hours != 0:
        work_time_info += f"{hours}h "
    if minutes != 0:
        work_time_info += f"{minutes}m "
    if seconds != 0:
        work_time_info += f"{seconds}s"

    return work_time_info

def ask(q: str, convert_to_bool: bool = True):
    answer = input(q)
    
    if convert_to_bool:
        return answer.lower() == "y"
    else:
        return answer

def create_file_if_not_exists(path: Path, default_content):
    if path.exists():
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    with open(path, "wb") as file:
        pickle.dump(default_content, file)
