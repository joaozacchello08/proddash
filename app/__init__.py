from flask import Flask, request, jsonify
from flask_cors import CORS
from .extensions import db, jwt
from .routes import register_routes
from .models import TokenBlocklist
import os

def create_app():
    app = Flask(__name__) 

    flask_env = os.environ.get("FLASK_ENV", "development")
    match(flask_env):
        case "development":
            app.config.from_object("config.DevelopmentConfig")
        
        case "dev_deploy":
            app.config.from_object("config.DeployDevConfig")

        case "production":
            app.config.from_object("config.ProductionConfig")

        case _:
            app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    register_routes(app)

    @app.route("/", methods=["GET"])
    def root():
        with open("./assets/index.html", "r", encoding="utf-8") as f:
            html = f.read()
        return html

    @app.before_request
    def secure_requests():
        allowed_ips = app.config["ALLOWED_IPS"]
        if request.remote_addr not in allowed_ips:
            return jsonify({ "message": "Unauthorized IP" }), 403
        
        # if not request.is_secure and app.env == "production":
        #     return jsonify({ "message": "Only HTTPS are accepted." }), 403
        
        api_key = request.headers.get("X-API-KEY")
        if api_key != app.config["SECRET_KEY"]:
            return jsonify({ "message": "API key invalid." }), 401 

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    return app
