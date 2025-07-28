from flask import Flask
from flask_cors import CORS
from .extensions import db, jwt
from .routes import register_routes
from .models import TokenBlocklist
import os

def create_app():
    app = Flask(__name__) 

    flask_env = os.environ.get("FLASK_ENV", "development")
    if flask_env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    register_routes(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    return app
