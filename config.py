from dotenv import load_dotenv, dotenv_values
from os import getenv

load_dotenv()
config = dotenv_values()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = config["DEVELOPMENT_SQLALCHEMY_DATABASE_URI"] | getenv("DEVELOPMENT_SQLALCHEMY_DATABASE_URI") 

class ProductionConfig(Config):
    pass
