import platform
from pathlib import Path
import os
import json

def get_programdata_path(appname: str = None) -> Path:
    system = platform.system()

    if system == "Windows":
        base = Path(os.environ.get("PROGRAMDATA", "C:\\ProgramData"))
    elif system == "Darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path.home() / ".local/share"

    return base / appname if appname else base

def get_db_path(apppath: str = None) -> None:
    return f"sqlite:///{(apppath / "proddash.db")}"

#region functions
def add_cfg(file_path: Path, data: dict = {}):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def edit_cfg(file_path: Path, updates: dict = {}):
    with open(file_path, "r+") as f:
        data = json.load(f)
        for key, value in updates.items():
            data[key] = value
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

def load_cfg(file_path: Path):
    with open(file_path, "r") as f:
        data = json.load(f)

    return data
#endregion
