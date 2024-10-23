from flask import Flask
from flask_socketio import SocketIO


class SocketIOApplication:
    def __init__(self, flask: Flask):
        self.io = SocketIO(cors_allowed_origins="*")
        self.io.init_app(flask)

        @self.io.on("connect")
        def handle_connect():
            print("Client connected")
            self.io.emit("response", {"message": "Connected successfully!"})

        @self.io.on("disconnect")
        def handle_disconnect():
            print("Client disconnected")
            pass

        @self.io.on("my_event")
        def handle_my_custom_event(json):
            print("received json: " + str(json))
            self.io.emit("response", {"message": "Message received"})
