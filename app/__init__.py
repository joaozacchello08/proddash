from flask import Flask, request, jsonify
from flask_cors import CORS
from .extensions import db, jwt
from .routes import register_routes
from .models import TokenBlocklist
import os

def create_app(name: str):
    app = Flask(name) 

    flask_env = os.environ.get("FLASK_ENV", "development")
    if flask_env == "production":
        app.config.from_object("config.ProductionCfg")
    else:
        app.config.from_object("config.DevelopmentCfg")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE"])
    register_routes(app)

    # @app.route("/", methods=["GET"])
    # def root():
    #     with open("./assets/index.html", "r", encoding="utf-8") as f:
    #         html = f.read()
    #     return html

    @app.before_request
    def secure_requests():
        if request.method == "OPTIONS":
            return

        # the service is working locally for now,
        # i dont think i need that amount of security

        # api_key = request.headers.get("X-API-KEY")
        # if api_key != app.config["SECRET_KEY"]:
        #     return jsonify({ "message": "API key invalid." }), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    return app
