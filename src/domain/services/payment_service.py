
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.payment_repository import PaymentRepository


class PaymentService(EntityServiceImpl):
    def __init__(self, payment_repository: PaymentRepository):
        super().__init__(payment_repository)

    
