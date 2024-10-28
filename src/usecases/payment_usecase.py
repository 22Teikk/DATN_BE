
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.payment_service import PaymentService

class PaymentUsecase(EntityUsecase):
    def __init__(self, payment_service: PaymentService):
        super().__init__(payment_service)
    
