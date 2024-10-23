from flask_restful import Api
from flask import Blueprint, Flask
from src.adapters.api.resources.user_locale_resource import UserLocaleResource
from src.containers.user_locale_container import UserLocaleContainer
from src.domain.schemas.user_locale_schema import UserLocaleSchema
from src.containers.userfile_container import UserfileContainer
from src.domain.schemas.userfile_schema import UserFileSchema
from src.containers.file_container import FileContainer
from src.containers.user_container import UserContainer
from src.domain.schemas.file_schema import FileSchema
from src.domain.schemas.user_schema import UserSchema
from src.containers.entity_container import EntityContainer
from src.domain.schemas.entity_schema import EntitySchema
from src.containers.repository_container import RepositoryContainer


class RestfullResourceContainer:
    pass
    # def __init__(
    #     self,
    #     flask_framework: Flask,
    #     repository_container: RepositoryContainer,
    #     url_prefix: str,
    # ):
    #     self.repository_container = repository_container
    #     self.blueprint = Blueprint(url_prefix, __name__, url_prefix=url_prefix)

    #     api = Api(self.blueprint)
    #     api.add_resource(
    #         EntityResource,
    #         f"/entities",
    #         f"/entities/<string:_id>",
    #         resource_class_args=(
    #             EntityContainer(self.repository_container),
    #             EntitySchema(),
    #         ),
    #         endpoint="entities",
    #     )

    #     api.add_resource(
    #         EntityResource,
    #         f"/users",
    #         f"/users/<string:_id>",
    #         resource_class_args=(
    #             UserContainer(self.repository_container),
    #             UserSchema(),
    #         ),
    #         endpoint="users",
    #     )

    #     api.add_resource(
    #         EntityResource,
    #         f"/files",
    #         f"/files/<string:_id>",
    #         resource_class_args=(
    #             FileContainer(),
    #             FileSchema(),
    #         ),
    #         endpoint="files",
    #     )
    #     flask_framework.register_blueprint(self.blueprint)
