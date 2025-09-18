import os
import platform
from pathlib import Path

def get_sqlite_uri(appname="ProdDash", dbname="proddash.db"):
    system = platform.system()

    if system == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / appname
    elif system == "Darwin":
        base = Path.home() / "Library/Application Support" / appname
    else:
        base = Path.home() / ".local/share" / appname

    base.mkdir(parents=True, exist_ok=True)

    db_path = base / dbname

    return f"sqlite:///{db_path.as_posix()}"
