import os

from src.domain.entities.cart import Cart
from src.domain.schemas.cart_schema import CartSchema
from src.domain.entities.wishlist import Wishlist
from src.domain.schemas.wishlist_schema import WishlistSchema
from src.domain.entities.store import Store
from src.domain.schemas.store_schema import StoreSchema
from src.domain.entities.user_profile import UserProfile
from src.domain.schemas.user_profile_schema import UserProfileSchema
from src.domain.entities.payment import Payment
from src.domain.schemas.payment_schema import PaymentSchema
from src.domain.entities.payment_method import PaymentMethod
from src.domain.schemas.payment_method_schema import PaymentMethodSchema
from src.domain.entities.role import Role
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
        self.role_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Role.__tablename__, Role), self._cache, CategorySchema()
        )
        self.payment_method_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(PaymentMethod.__tablename__, PaymentMethod), self._cache, PaymentMethodSchema()
        )
        self.payment_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Payment.__tablename__, Payment), self._cache, PaymentSchema()
        )
        self.user_profile_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(UserProfile.__tablename__, UserProfile), self._cache, UserProfileSchema()
        )
        self.store_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Store.__tablename__, Store), self._cache, StoreSchema()
        )
        self.wishlist_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Wishlist.__tablename__, Wishlist), self._cache, WishlistSchema()
        )
        self.cart_repository = MySQLRepository(
            self.sqldb.get_session(), self.sqldb.get_table(Cart.__tablename__, Cart), self._cache, CartSchema()
        )