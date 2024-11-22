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
        self.flask.add_url_rule("/upload_files", view_func=self.upload_files, methods=["POST"])

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
    
    def upload_files(self):
        if 'files' not in request.files:
            return {"error": "No file part in request"}, 400

        files = request.files.getlist('files')
        if len(files) == 0:
            return {"error": "No files selected"}, 400

        uploaded_files = []
        upload_dir = os.path.join(os.getcwd(), "static")  # Thư mục lưu trữ file
        os.makedirs(upload_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        for file in files:
            if file.filename == '':
                continue  # Bỏ qua file không có tên

            # Tạo tên file an toàn và lưu trữ
            file_extension = os.path.splitext(file.filename)[1]
            safe_filename = secure_filename(f"uploaded_{get_new_uuid()}{file_extension}")
            file_path = os.path.join(upload_dir, safe_filename)
            file.save(file_path)

            # Thêm đường dẫn file vào danh sách kết quả
            file_url = f"{Config.APP_HOST}/files/{safe_filename}"
            uploaded_files.append(file_url)

        if not uploaded_files:
            return {"error": "No valid files uploaded"}, 400

        return {"data": uploaded_files}, 200