# server/app/__init__.py


import os
from flask import Flask, jsonify
from flask_redis import FlaskRedis
from fakeredis import FakeStrictRedis
from db import db
from app.extensions import (
    bcrypt,
    migrate,
    jwt,
    redis_client
)
from app.api.users import users_blueprint


def create_app(script_info=None):
    """Application factory."""
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    if app.config["TESTING"]:
        redis_store = FlaskRedis.from_custom_provider(FakeStrictRedis)
    else:
        redis_store = redis_client
    redis_store.init_app(app)

    # register blueprints
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        from app.api.users.models import User
        return {"app": app, "db": db, "User": User, "redis_store": redis_store}

    @app.route("/ping", methods=["GET"])
    def ping_pong():
        """Check application"s health"""
        return jsonify({
            "status": "success",
            "message": "pong!"
        })
    return app
