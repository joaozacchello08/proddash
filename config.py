import os
from get_sqlite_uri import get_sqlite_uri
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

class DevelopmentCfg(Config):
    # SQLALCHEMY_DATABASE_URI = get_sqlite_uri()
    SQLALCHEMY_DATABASE_URI = os.getenv("SUPABASE_URI")

class ProductionCfg(Config):
    pass
