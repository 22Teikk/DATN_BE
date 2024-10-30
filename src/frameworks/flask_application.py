from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from src.containers.route_container import RouteContainer
from src.containers.blueprint_container import BlueprintContainer
from src.containers.repository_container import RepositoryContainer



class FlaskApplication:
    def __init__(self):
        self.framework = Flask(__name__)
        self.framework.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
        JWTManager(self.framework)
        self.repository_container = RepositoryContainer()
        self.route_container = RouteContainer(self.framework)
        self.blueprint_container = BlueprintContainer(
            self.framework, self.repository_container
        )
