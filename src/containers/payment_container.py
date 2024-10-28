
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.payment_service_impl import PaymentServiceImpl
from src.usecases.payment_usecase import PaymentUsecase

class PaymentContainer:
    def __init__(self, repository_container: RepositoryContainer):
        service = PaymentServiceImpl(repository_container.payment_repository)
        self.usecase = PaymentUsecase(service)

    
