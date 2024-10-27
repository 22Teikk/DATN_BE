import os

from src.domain.schemas.category_schema import CategorySchema
from src.domain.schemas.discount_schema import DiscountSchema
from src.domain.schemas.entity_schema import EntitySchema
from src.domain.schemas.product_schema import ProductSchema
from src.domain.entities.product import Product
from src.domain.entities.discount import Discount
from src.domain.entities.category import Category
from src.domain.entities.entity import Entity
from src.adapters.repositories.mysql_repository import MySQLRepository
from src.adapters.database.mysql import MySQL
from src.adapters.database.redis import Redis
from src.adapters.repositories.mongo_repository import MongoRepository
from src.adapters.database.mongodb import MongoDB
from src.adapters.repositories.redis_cache import RedisCache



class RepositoryContainer:
    def __init__(self):
        self._cache = RedisCache(Redis())
        self.mongodb = MongoDB()
        self.sqldb = MySQL()
        self.init_collections()
        self.init_tables()

    def init_collections(self):
        pass
        # self.entity_repository = MongoRepository(
        #     self.mongodb.get_collection("entities"), self._cache
        # )

    def init_tables(self):
        self.entity_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Entity.__tablename__, Entity), self._cache, EntitySchema()
        )
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>> Session type: {type(self.sqldb.session)}")

        self.category_repository = MySQLRepository(
            self.sqldb.get_session(),self.sqldb.get_table(Category.__tablename__, Category), self._cache, CategorySchema()
        )
        self.discount_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Discount.__tablename__, Discount), self._cache, DiscountSchema()
        )
        self.product_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Product.__tablename__, Product), self._cache, ProductSchema()
        )