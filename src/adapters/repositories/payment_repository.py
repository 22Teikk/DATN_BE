
from src.adapters.repositories.entity_repository import EntityRepository
from pymongo.collection import Collection

class PaymentRepository(EntityRepository):
    def __init__(self, collection: Collection):
        self.collection = collection
    
