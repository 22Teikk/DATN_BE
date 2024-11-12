import os
from flask import Flask, request, send_from_directory
from config import Config
from src.domain.entities.utils import get_new_uuid, get_current_timestamp_str
from werkzeug.utils import secure_filename


class RouteContainer:
    def __init__(self, flask: Flask):
        self.flask = flask
        self.flask.add_url_rule("/", view_func=self.index)
        self.flask.add_url_rule("/uid", view_func=self.uid)
        self.flask.add_url_rule("/protected", view_func=self.protected_route)
        self.flask.add_url_rule("/files/<string:file>", view_func=self.custom_static)
        self.flask.add_url_rule("/upload", view_func=self.upload_file, methods=["POST"])

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

    def upload_file(self):
        if 'file' not in request.files:
            return {"error": "No file part in request"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400

        # Secure the filename and determine the upload path
        file_extension = os.path.splitext(file.filename)[1]
        safe_filename = secure_filename(f"uploaded_{get_new_uuid()}{file_extension}")
        upload_dir = os.path.join(os.getcwd(), "static")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, safe_filename)
        
        # Save the file and return the file URL
        file.save(file_path)
        return {"data": f"{Config.APP_HOST}/files/{safe_filename}"}, 200