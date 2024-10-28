from flask import Blueprint, Flask
from flask_restx import Api

from src.adapters.api.namespace.store_namespace import StoreNamespace
from src.containers.store_container import StoreContainer
from src.domain.schemas.store_schema import StoreSchema
from src.adapters.api.namespace.user_profile_namespace import UserProfileNamespace
from src.containers.user_profile_container import UserProfileContainer
from src.domain.schemas.user_profile_schema import UserProfileSchema
from src.adapters.api.namespace.payment_namespace import PaymentNamespace
from src.containers.payment_container import PaymentContainer
from src.domain.schemas.payment_schema import PaymentSchema
from src.adapters.api.namespace.payment_method_namespace import PaymentMethodNamespace
from src.containers.payment_method_container import PaymentMethodContainer
from src.domain.schemas.payment_method_schema import PaymentMethodSchema
from src.containers.role_container import RoleContainer
from src.domain.schemas.role_schema import RoleSchema
from src.adapters.api.namespace.role_namespace import RoleNamespace
from src.adapters.api.namespace.product_namespace import ProductNamespace
from src.containers.product_container import ProductContainer
from src.domain.schemas.product_schema import ProductSchema
from src.adapters.api.namespace.discount_namespace import DiscountNamespace
from src.containers.discount_container import DiscountContainer
from src.domain.schemas.discount_schema import DiscountSchema
from src.adapters.api.namespace.category_namespace import CategoryNamespace
from src.containers.category_container import CategoryContainer
from src.domain.schemas.category_schema import CategorySchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace
from src.containers.entity_container import EntityContainer
from src.containers.repository_container import RepositoryContainer
from src.domain.schemas.entity_schema import EntitySchema


class NamespaceContainer:
    def __init__(
        self,
        flask_framework: Flask,
        repository_container: RepositoryContainer,
        url_prefix: str,
    ):
        self.repository_container = repository_container
        self.blueprint = Blueprint(url_prefix, __name__, url_prefix=url_prefix)

        self.api = Api(
            self.blueprint,
            version="1.0",
            title="Hihoay API",
            doc="/help",
            description="Hihoay API",
            consumes=[
                "application/json"
            ],  # Yêu cầu Content-Type là application/json cho toàn bộ API
            security="Bearer Auth",  # Thêm thông tin bảo mật cho tài liệu Swagger
            authorizations={
                "Bearer Auth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "description": "Add a Bearer token in the format: Bearer <token>",
                }
            },
        )
        self.init_namespace()
        flask_framework.register_blueprint(self.blueprint)

    def init_namespace(self):
        EntityNamespace(
            container=EntityContainer(self.repository_container),
            schema=EntitySchema(),
            api=self.api,
            namespace_name="entities",
            entity_name="Entity",
        )
        CategoryNamespace(
            container=CategoryContainer(self.repository_container),
            schema=CategorySchema(),
            api=self.api,
            namespace_name="categories",
            entity_name="Category",
        )
        DiscountNamespace(
            container=DiscountContainer(self.repository_container),
            schema=DiscountSchema(),
            api=self.api,
            namespace_name="discounts",
            entity_name="Discount",
        )
        ProductNamespace(
            container=ProductContainer(self.repository_container),
            schema=ProductSchema(),
            api=self.api,
            namespace_name="products",
            entity_name="Product",
        )
        RoleNamespace(
            container=RoleContainer(self.repository_container),
            schema=RoleSchema(),
            api=self.api,
            namespace_name="roles",
            entity_name="Role",
        )
        PaymentMethodNamespace(
            container=PaymentMethodContainer(self.repository_container),
            schema=PaymentMethodSchema(),
            api=self.api,
            namespace_name="payment_methods",
            entity_name="PaymentMethod",
        )
        PaymentNamespace(
            container=PaymentContainer(self.repository_container),
            schema=PaymentSchema(),
            api=self.api,
            namespace_name="payments",
            entity_name="Payment",
        )
        UserProfileNamespace(
            container=UserProfileContainer(self.repository_container),
            schema=UserProfileSchema(),
            api=self.api,
            namespace_name="user_profiles",
            entity_name="UserProfile",
        )
        StoreNamespace(
            container=StoreContainer(self.repository_container),
            schema=StoreSchema(),
            api=self.api,
            namespace_name="stores",
            entity_name="Store",
        )