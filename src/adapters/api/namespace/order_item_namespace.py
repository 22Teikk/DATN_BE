from flask import request
from flask_restx import Api, Resource
from src.containers.order_item_container import OrderItemContainer
from src.domain.schemas.order_item_schema import OrderItemSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class OrderItemNamespace(EntityNamespace):
    def __init__(
        self,
        container: OrderItemContainer,
        schema: OrderItemSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

        @self.namespace.route("/user")
        class CartOfUser(Resource):
            @self.namespace.doc(f"list_{entity_name}_by_user", security="Bearer Auth")
            @self.namespace.param("uid", "User ID")
            @self.namespace.response(200, f"{entity_name} retrieved")
            @self.namespace.response(404, f"{entity_name} not found")
            @self.namespace.response(401, "Unauthorized")
            def get(self):
                uid = request.args.get("order_id")
                if uid:
                    items = container.usecase.find_by_query({"order_id" : uid})
                    return schema.dump(items, many=True), 200
                else:
                    return {"error": "User ID not provided"}, 400