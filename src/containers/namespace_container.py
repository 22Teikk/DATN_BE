from flask import Blueprint, Flask
from flask_restx import Api

from src.adapters.api.namespace.categories_namespace import CategoriesNamespace
from src.containers.categories_container import CategoriesContainer
from src.domain.schemas.categories_schema import CategoriesSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace
from src.containers.entity_container import EntityContainer
from src.containers.repository_container import RepositoryContainer
from src.domain.schemas.entity_schema import EntitySchema


class NamespaceContainer:
    def __init__(
        self,
        flask_framework: Flask,
        repository_container: RepositoryContainer,
        url_prefix: str,
    ):
        self.repository_container = repository_container
        self.blueprint = Blueprint(url_prefix, __name__, url_prefix=url_prefix)

        self.api = Api(
            self.blueprint,
            version="1.0",
            title="Hihoay API",
            doc="/help",
            description="Hihoay API",
            consumes=[
                "application/json"
            ],  # Yêu cầu Content-Type là application/json cho toàn bộ API
            security="Bearer Auth",  # Thêm thông tin bảo mật cho tài liệu Swagger
            authorizations={
                "Bearer Auth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "Add a Bearer token in the format: Bearer <token>",
                }
            },
        )
        self.init_namespace()
        flask_framework.register_blueprint(self.blueprint)

    def init_namespace(self):
        EntityNamespace(
            container=EntityContainer(self.repository_container),
            schema=EntitySchema(),
            api=self.api,
            namespace_name="entities",
            entity_name="Entity",
        )
        CategoriesNamespace(
            container=CategoriesContainer(self.repository_container),
            schema=CategoriesSchema(),
            api=self.api,
            namespace_name="categories",
            entity_name="Category",
        )