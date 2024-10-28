
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.payment_method_service import PaymentMethodService

class PaymentMethodUsecase(EntityUsecase):
    def __init__(self, payment_method_service: PaymentMethodService):
        super().__init__(payment_method_service)
    
