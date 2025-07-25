class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://xongs:0069@localhost:5432/proddash_dev"

class ProductionConfig(Config):
    pass
