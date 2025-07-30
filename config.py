from dotenv import load_dotenv
from os import getenv

load_dotenv()

USER = getenv("user")
PASSWORD = getenv("password")
HOST = getenv("host")
PORT = getenv("port")
DBNAME = getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv("SECRET_KEY")
    ALLOWED_IPS = getenv("ALLOWED_IPS").split(",")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DEVELOPMENT_SQLALCHEMY_DATABASE_URI")

class DeployDevConfig(Config):
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

class ProductionConfig(Config):
    pass
