import os
from src.domain.entities.utils import schema_to_restx_model
from src.domain.schemas.entity_schema import EntitySchema
from src.containers.entity_container import EntityContainer
from flask import request
from flask_restx import Api, Resource, ValidationError, fields


class EntityNamespace:
    def __init__(
        self,
        container: EntityContainer,
        schema: EntitySchema,
        api: Api,
        namespace_name: str,
        entity_name: str,
    ):
        self.container = container
        model = schema_to_restx_model(schema, entity_name, api)

        namespace = api.namespace(
            namespace_name, description=f"{namespace_name} operations"
        )
        self.model = model
        self.namespace = namespace

        @namespace.route("/")
        class EntityList(Resource):
            @namespace.doc(f"list_{entity_name}", security="Bearer Auth")
            @namespace.response(200, f"{entity_name} retrieved")
            @namespace.response(404, f"{entity_name} not found")
            @namespace.response(401, "Unauthorized")
            def get(self):
                auth_user = request.headers.get("Authorization")
                print(auth_user)
                if auth_user == os.getenv("ADMIN_TOKEN", ""):
                    items = container.usecase.find_by_query()
                    if items:
                        results = schema.dump(items, many=True)
                        print(items, results)
                        return results, 200
                    else:
                        return {"error": "Item not found"}, 404
                else:
                    return {"error": "Unauthorized"}, 401

            @namespace.doc(f"create_{entity_name}")
            @namespace.expect(model)
            @namespace.response(201, f"{entity_name} created")
            @namespace.response(400, "Invalid input")
            @namespace.response(409, f"{entity_name} already exists")
            @namespace.response(404, f"{namespace_name} not found")
            @namespace.response(500, "Internal server error")
            def post(self):
                data = request.get_json()
                if data is None:
                    return {"error": "No input data provided"}, 400
                try:
                    valid_data = schema.load(data)
                except Exception as err:
                    return {"error": err.messages}, 400
                try:
                    inserted_id = container.usecase.insert(valid_data)
                    if inserted_id == -1:
                        return {"error": "Item with this _id already exists"}, 409
                    return {"_id": inserted_id}, 201
                except Exception as e:
                    return {"error": "Internal server error", "message": str(e)}, 500

        @namespace.route("/<string:_id>")
        class Entity(Resource):
            @namespace.doc(f"get_{entity_name}")
            @namespace.response(200, f"{entity_name} retrieved")
            @namespace.response(404, f"{entity_name} not found")
            def get(self, _id=None):
                if _id:
                    item = container.usecase.find_by_id(_id)
                    if not item:
                        return {"error": "Item not found"}, 404
                    return schema.dump(item), 200
                return {"error": "Item not found"}, 404

            @namespace.doc(f"update_{entity_name}", consumes=["application/json"])
            @namespace.response(200, f"{entity_name} updated")
            @namespace.response(404, f"{entity_name} not found")
            @namespace.response(400, "Invalid input")
            @namespace.expect(model)
            def put(self, _id):
                # Lấy dữ liệu JSON từ yêu cầu

                data_update_request = request.get_json()
                data_saved = container.usecase.find_by_id(_id)
                print("data_saved", data_saved)
                print("data_update_request", data_update_request)
                if not data_saved:
                    return {"error": f"{entity_name} not found"}, 404

                try:
                    # Xác thực và tuần tự hóa dữ liệu với schema
                    data_saved.update(data_update_request)
                    valid_data = schema.load(data_saved)
                    print(valid_data)
                    # Nếu valid_data là dict, cập nhật _id
                    if isinstance(valid_data, dict):
                        valid_data["_id"] = _id
                        data_saved.update(valid_data)
                    else:
                        # Nếu valid_data là một đối tượng, gán _id vào thuộc tính _id của nó
                        valid_data._id = _id
                        data_saved.update(valid_data)

                    print(valid_data)
                except Exception as e:
                    # Trả về lỗi 500 cho các lỗi khác
                    print(f"Internal Server Error: {str(e)}")
                    return {"error": "Internal server error", "message": str(e)}, 400

                # Tiến hành cập nhật thông qua usecase
                updated = container.usecase.update(data_saved)
                print("updated", updated, data_saved)
                if updated:
                    return {"updated": updated}, 200
                else:
                    # Trả về lỗi 404 nếu không tìm thấy thực thể cần cập nhật
                    return {"error": f"{entity_name} not found"}, 404

            @namespace.doc(f"delete_{entity_name}")
            @namespace.response(204, f"{entity_name} deleted")
            @namespace.response(404, f"{entity_name} not found")
            def delete(self, _id):
                result = container.usecase.delete(_id)
                if result == 0:
                    return {"error": "Item not found"}, 404
                return {"message": "Item deleted"}, 204

        self.entity_list = EntityList
        self.entity = Entity
