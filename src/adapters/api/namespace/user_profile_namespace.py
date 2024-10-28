import datetime
from flask_restx import Api
from src.containers.user_profile_container import UserProfileContainer
from src.domain.schemas.user_profile_schema import UserProfileSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class UserProfileNamespace(EntityNamespace):
    def __init__(
        self,
        container: UserProfileContainer,
        schema: UserProfileSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)
        self.entity.get = self.custom_get_entity

    def custom_get_entity(self, _id=None):
        if _id:
            print(">>>>>>>ID: " + _id)
            item = self.container.usecase.find_by_id(_id)
            if not item:
                return {"error": "Item not found"}, 404

            # Kiểm tra và chuyển đổi kiểu dữ liệu cho các trường DateTime
            if isinstance(item['created_at'], str):
                item['created_at'] = datetime.datetime.fromisoformat(item['created_at'])

            print(">>>>>>>>> Item: ", item)
            return self.schema.dump(item), 200
            
        return {"error": "Item not found"}, 404
