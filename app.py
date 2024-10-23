import os
from src.frameworks.flask_application import FlaskApplication
from src.frameworks.socket_io_application import SocketIOApplication


if __name__ == "__main__":
    flask_app = FlaskApplication()
    socket = SocketIOApplication(flask_app.framework)

    socket.io.run(
        flask_app.framework,
        debug=(
            True
        ),
        host="0.0.0.0",
        port=8080,
        allow_unsafe_werkzeug=True,
        use_reloader=False,
    )
