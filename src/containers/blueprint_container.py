from flask import Blueprint, Flask
from src.containers.namespace_container import NamespaceContainer
from src.containers.repository_container import RepositoryContainer


class BlueprintContainer:
    def __init__(
        self, flask_framework: Flask, repository_container: RepositoryContainer
    ):
        self.flask_framework = flask_framework
        self.repository_container = repository_container
        self.namespace_container = NamespaceContainer(
            self.flask_framework,
            self.repository_container,
            "/api/v1",
        )
