import datetime
from flask_restx import Api
from src.containers.discount_container import DiscountContainer
from src.domain.schemas.discount_schema import DiscountSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class DiscountNamespace(EntityNamespace):
    def __init__(
        self,
        container: DiscountContainer,
        schema: DiscountSchema,
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
            if isinstance(item['start_date'], str):
                item['start_date'] = datetime.datetime.fromisoformat(item['start_date'])
            if isinstance(item['end_date'], str):
                item['end_date'] = datetime.datetime.fromisoformat(item['end_date'])

            print(">>>>>>>>> Item: ", item)
            return self.schema.dump(item), 200
            
        return {"error": "Item not found"}, 404

