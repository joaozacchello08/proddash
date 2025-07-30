from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv("SECRET_KEY")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DEVELOPMENT_SQLALCHEMY_DATABASE_URI")
    ALLOWED_IPS = getenv("ALLOWED_IPS").split(",")

class DeployDevConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DEPLOY_DEV_SQLALCHEMY_DATABASE_URI")

class ProductionConfig(Config):
    pass
