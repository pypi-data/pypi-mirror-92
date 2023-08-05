import platform
from enum import Enum
from typing import Tuple


class OsName(Enum):
    Windows: str = 'win'
    Linux: str = 'linux'
    Mac: str = 'mac'


def get_platform() -> Tuple[OsName, bool]:
    _system = platform.system()
    if _system == "Windows":
        _system = OsName.Windows
    elif _system == "Linux":
        _system = OsName.Linux
    elif _system == "Darwin":
        _system = OsName.Mac

    return _system, platform.machine().endswith('64')
