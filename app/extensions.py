from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from flask_jwt_extended import JWTManager

db = SQLAlchemy(model_class=declarative_base())
jwt = JWTManager()
