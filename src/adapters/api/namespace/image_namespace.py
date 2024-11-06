from http import HTTPStatus
import os
from flask import json, request, send_from_directory
from flask_restx import Api, Resource
from config import Config
from src.containers.feedback_container import FeedbackContainer
from src.containers.product_container import ProductContainer
from src.domain.entities.image import Image
from src.domain.entities.utils import get_new_uuid
from src.containers.image_container import ImageContainer
from src.domain.schemas.image_schema import ImageSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class ImageNamespace(EntityNamespace):
    def __init__(
        self,
        container: ImageContainer,
        feedback_container: FeedbackContainer,
        product_container: ProductContainer,
        schema: ImageSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)
        self.feedback_container = feedback_container
        self.product_container = product_container
        self.entity_list.post = self.custom_post
    def custom_post(self):
        response_data = []
        # File information json
        feedback_id = request.form.get("feedback_id")
        product_id = request.form.get("product_id")
        files_received = request.files.getlist("files")
        if files_received:
            for i in range(len(files_received)):
                file = files_received[i]
                try:
                    new_file = self.schema.dump(self.update_file_info(feedback_id, product_id, file))
                    response_data.append(new_file)
                except Exception as err:
                    return {"error": str(err)}, 400
            self.container.usecase.upserts(datas=response_data)
            return response_data, HTTPStatus.CREATED
        else:
            return {"error": "No data received or files"}, HTTPStatus.BAD_REQUEST

    def update_file_info(self, feedback_id, product_id, file) -> Image:
        id = str(get_new_uuid())
        folder = f"static"
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_extension = os.path.splitext(file.filename)[1] 
        file_path = os.path.join(folder, id + file_extension)
        file.save(file_path)
        url = Config.APP_HOST + "/files/" + id + file_extension
        image_file = Image(id, url)
        if feedback_id:
            image_file.feedback_id = feedback_id
        if product_id:
            image_file.product_id = product_id
        return image_file