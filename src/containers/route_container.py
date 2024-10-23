import os
from flask import Flask, request, send_from_directory
from src.domain.entities.utils import get_new_uuid


class RouteContainer:
    def __init__(self, flask: Flask):
        self.flask = flask
        self.flask.add_url_rule("/", view_func=self.index)
        self.flask.add_url_rule("/version", view_func=self.version)
        self.flask.add_url_rule("/uid", view_func=self.uid)
        self.flask.add_url_rule("/protected", view_func=self.protected_route)
        self.flask.add_url_rule("/files/<path:path>", view_func=self.custom_static)

    def index(self):
        return "Hello, World!", 200

    def version(self):
        return (
            "App: "
            + os.getenv("APP_NAME")
            + " - env: "
            + os.getenv("ENV")
            + " - version: "
            + os.getenv("APP_VERSION"),
            200,
        )

    def uid(self):
        return get_new_uuid(), 200

    def require_auth(self, f):
        def decorator(*args, **kwargs):
            auth_key = request.headers.get("Auth-Key")
            if auth_key != self.flask.config["AUTH_KEY"]:
                return {"error": "Unauthorized"}, 401
            return f(*args, **kwargs)

        return decorator

    def protected_route(self):
        return {"message": "You have access to this route"}, 401

    def custom_static(self, path):
        print("custom_static", path)
        directory = os.path.join(os.getcwd(), "static")
        print(os.getcwd())
        return send_from_directory(directory, path)
