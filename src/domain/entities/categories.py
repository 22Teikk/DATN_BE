
from src.domain.entities.entity import Entity

class Categories(Entity):
    def __init__(
        self, 
        _id: str,
        category_name: str):
        super().__init__(_id)
        self.category_name = category_name
