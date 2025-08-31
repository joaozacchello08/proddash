import os
from get_sqlite_uri import get_sqlite_uri

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

class DevelopmentCfg(Config):
    SQLALCHEMY_DATABASE_URI = get_sqlite_uri()

class ProductionCfg(Config):
    pass
