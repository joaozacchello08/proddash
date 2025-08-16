import os
from config_functions import get_programdata_path, load_cfg

app_path = get_programdata_path("ProdDash")
cfg_file_path = app_path / "app_cfg.json" # json
app_path.mkdir(parents=True, exist_ok=True)

cfg = load_cfg(cfg_file_path)

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

class DevelopmentCfg(Config):
    SQLALCHEMY_DATABASE_URI = cfg["db_uri"]

class ProductionCfg(Config):
    pass
