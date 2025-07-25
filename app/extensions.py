from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

db = SQLAlchemy(model_class=declarative_base())
