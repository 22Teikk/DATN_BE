from flask import request
from flask_restx import Api, Resource
from src.containers.working_container import WorkingContainer
from src.domain.schemas.working_schema import WorkingSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class WorkingNamespace(EntityNamespace):
    def __init__(
        self,
        container: WorkingContainer,
        schema: WorkingSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

        @self.namespace.route("/type")
        class WorkingByType(Resource):
            def get(self):
                user_id = request.args.get("user_id")
                type = request.args.get("type")
                working_list = container.usecase.find_by_query({
                    "user_id": user_id,
                    "type": type,
                })
                if working_list:
                    return schema.dump(working_list, many=True), 200
                else:
                    return {"error": f"No {entity_name} found for user_id {user_id} and type {type}"}, 400