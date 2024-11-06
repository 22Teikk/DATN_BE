import os
from src.adapters.database.mysql import MySQL
from src.frameworks.flask_application import FlaskApplication
from src.frameworks.socket_io_application import SocketIOApplication
import logging

# logging.basicConfig(filename='record.log',
#                 level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

if __name__ == "__main__":
    flask_app = FlaskApplication()
    socket = SocketIOApplication(flask_app.framework)

    socket.io.run(
        flask_app.framework,
        host="0.0.0.0",
        port=5001,
        allow_unsafe_werkzeug=True,
        use_reloader=False,
    )
