from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(kw_only=True)
class CoreSettings:
    data_file: Path
    echo: Optional[bool] = False

@dataclass(kw_only=True)
class Config:
    core: CoreSettings
