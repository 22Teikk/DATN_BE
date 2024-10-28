
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.payment_method_repository import PaymentMethodRepository


class PaymentMethodService(EntityServiceImpl):
    def __init__(self, payment_method_repository: PaymentMethodRepository):
        super().__init__(payment_method_repository)

    
