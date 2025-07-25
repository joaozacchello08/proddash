from flask import Flask, jsonify
from flask_cors import CORS
from .extensions import db
from .routes import register_routes
import os

def create_app():
    app = Flask(__name__) 

    flask_env = os.environ.get("FLASK_ENV", "development")
    if flask_env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")


    db.init_app(app)
    CORS(app)
    register_routes(app)

    #region errors handler
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({ "error": "Bad request." }), 400

    @app.errorhandler(403)
    def not_authorized(error):
        return jsonify({ "error": "Permission denied." }), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({ "error": "Not found." }), 404
    
    @app.errorhandler(409)
    def already_exists(error):
        return jsonify({ "error": "Already exists." }), 409

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return jsonify({ "error": "Internal server error." }), 500
    #endregion

    return app
