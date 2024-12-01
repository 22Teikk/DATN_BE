from flask import request
from flask_restx import Api, Resource
from src.domain.entities.utils import get_new_uuid
from src.containers.cart_container import CartContainer
from src.containers.order_container import OrderContainer
from src.domain.schemas.order_schema import OrderSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class OrderNamespace(EntityNamespace):
    def __init__(
        self,
        container: OrderContainer,
        cart_container: CartContainer,
        schema: OrderSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        self.cart_container = cart_container  # Thêm cart_container vào tham số container cho OrderNamespace
        super().__init__(container, schema, api, namespace_name, entity_name)
        self.entity_list.post = self.create_order

        @self.namespace.route("/user")
        class CartOfUser(Resource):
            @self.namespace.doc(f"list_{entity_name}_by_user", security="Bearer Auth")
            @self.namespace.param("uid", "User ID")
            @self.namespace.response(200, f"{entity_name} retrieved")
            @self.namespace.response(404, f"{entity_name} not found")
            @self.namespace.response(401, "Unauthorized")
            def get(self):
                uid = request.args.get("uid")
                if uid:
                    items = container.usecase.find_by_query({"user_id" : uid})
                    return schema.dump(items, many=True), 200
                else:
                    return {"error": "User ID not provided"}, 400
                
    def create_order(self):
        data = request.get_json()
        if data is None:
            return {"error": "No input data provided"}, 400
        try:
            data['_id'] = get_new_uuid()
            print(data['_id'])
            valid_data = self.schema.load(data)
        except Exception as err:
            return {"error": err.messages}, 400
        try:
            inserted_id = self.container.usecase.insert(valid_data)
            if inserted_id == -1:
                return {"error": "Item with this _id already exists"}, 409
            self.cart_container.usecase.delete(valid_data["user_id"])
            return {"_id": inserted_id}, 201
        except Exception as e:
            return {"error": "Internal server error", "message": str(e)}, 500