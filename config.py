from dotenv import load_dotenv
from os import environ, getenv
from getpass import getuser

load_dotenv()

# get user programdata path
import platform
from pathlib import Path

def get_programdata_path(appname: str = None) -> Path:
    system = platform.system()

    if system == "Windows":
        base = Path(environ.get("PROGRAMDATA", "C:\\ProgramData"))
    elif system == "Darwin":  # macOS
        # Usa a pasta do usuário, não do sistema!
        base = Path.home() / "Library/Application Support"
    else:  # Linux
        base = Path.home() / ".local/share"

    return base / appname if appname else base

#endregion

# register or load our program data
app_path = get_programdata_path("ProdDash")
cfg_file_path = app_path / "app.cfg"
username = getuser()

app_path.mkdir(parents=True, exist_ok=True)

if not cfg_file_path.exists():
    with open(cfg_file_path, "w") as file:
        file.write(f"user={username}\n")
        file.write(f"db_path=sqlite:///{(app_path / f'proddash_user_{username}.db')}\n")

# load user program data
def load_cfg_file(path: Path) -> dict:
    data = {}
    if path.exists():
        with open(path) as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key] = value
    return data
#endregion

config_data = load_cfg_file(cfg_file_path)
# print(config_data)

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv("SECRET_KEY")

class DevelopmentCfg(Config):
    SQLALCHEMY_DATABASE_URI = config_data.get("db_path")

class ProductionCfg(Config):
    pass
