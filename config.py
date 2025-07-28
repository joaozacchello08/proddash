from dotenv import load_dotenv, dotenv_values
from os import getenv

load_dotenv()
config = dotenv_values()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config["SECRET_KEY"] if config["SECRET_KEY"] else getenv("SECRET_KEY")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = config["DEVELOPMENT_SQLALCHEMY_DATABASE_URI"] if config["DEVELOPMENT_SQLALCHEMY_DATABASE_URI"] else getenv("DEVELOPMENT_SQLALCHEMY_DATABASE_URI") 

class ProductionConfig(Config):
    pass
