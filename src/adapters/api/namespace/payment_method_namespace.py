from flask_restx import Api
from src.containers.payment_method_container import PaymentMethodContainer
from src.domain.schemas.payment_method_schema import PaymentMethodSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class PaymentMethodNamespace(EntityNamespace):
    def __init__(
        self,
        container: PaymentMethodContainer,
        schema: PaymentMethodSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

