from flask_restx import Api
from src.containers.role_container import RoleContainer
from src.domain.schemas.role_schema import RoleSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class RoleNamespace(EntityNamespace):
    def __init__(
        self,
        container: RoleContainer,
        schema: RoleSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

