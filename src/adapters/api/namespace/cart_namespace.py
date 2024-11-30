from flask import request
from flask_restx import Api, Resource
from src.containers.cart_container import CartContainer
from src.domain.schemas.cart_schema import CartSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class CartNamespace(EntityNamespace):
    def __init__(
        self,
        container: CartContainer,
        schema: CartSchema,
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
                uid = request.args.get("uid")
                if uid:
                    items = container.usecase.find_by_query({"user_id" : uid})
                    return schema.dump(items, many=True), 200
                else:
                    return {"error": "User ID not provided"}, 400
                
            def post(self):
                data = request.get_json()
                if data is None:
                    return {"error": "No input data provided"}, 400
                try:
                    valid_data = schema.load(data, many=True)
                    response = container.usecase.upserts(valid_data)
                    if response.get("status") == "success":
                        return {"message": "Carts update successfully"}, 201
                    else:
                        return {"error": response}, 500
                except Exception as e:
                    return {"error": str(e)}, 400

