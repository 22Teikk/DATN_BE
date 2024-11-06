import os
from flask import Flask, request, send_from_directory
from config import Config
from src.domain.entities.utils import get_new_uuid


class RouteContainer:
    def __init__(self, flask: Flask):
        self.flask = flask
        self.flask.add_url_rule("/", view_func=self.index)
        self.flask.add_url_rule("/uid", view_func=self.uid)
        self.flask.add_url_rule("/protected", view_func=self.protected_route)
        self.flask.add_url_rule("/files/<string:file>", view_func=self.custom_static)

    def index(self):
        return "Hello, World!", 200

    def uid(self):
        return get_new_uuid(), 200


    def protected_route(self):
        return {"message": "You have access to this route"}, 401

    def custom_static(self, file):
        print("custom_static", file)
        directory = os.path.join(os.getcwd(), "static")
        print(os.getcwd())
        return send_from_directory(directory, file)
