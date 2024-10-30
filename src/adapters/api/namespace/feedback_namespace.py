from flask_restx import Api
from src.containers.feedback_container import FeedbackContainer
from src.domain.schemas.feedback_schema import FeedbackSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class FeedbackNamespace(EntityNamespace):
    def __init__(
        self,
        container: FeedbackContainer,
        schema: FeedbackSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

