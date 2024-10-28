
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.payment_method_service_impl import PaymentMethodServiceImpl
from src.usecases.payment_method_usecase import PaymentMethodUsecase

class PaymentMethodContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = PaymentMethodServiceImpl(repository_container.payment_method_repository)
        self.usecase = PaymentMethodUsecase(service)

    
