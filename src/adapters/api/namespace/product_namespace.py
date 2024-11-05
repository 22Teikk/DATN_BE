from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Api, Resource
from sqlalchemy import func
from src.domain.entities.feedback import Feedback
from src.domain.entities.product import Product
from src.containers.product_container import ProductContainer
from src.domain.schemas.product_schema import ProductSchema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class ProductNamespace(EntityNamespace):
    def __init__(
        self,
        container: ProductContainer,
        schema: ProductSchema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

        @self.namespace.route('/search')
        class SearchResource(Resource):
            @self.namespace.doc(f"list_{entity_name}", security="Bearer Auth")
            @self.namespace.param("name", "Search by product name")
            @self.namespace.param("category", "Filter by category ID")
            @self.namespace.param("min_price", "Minimum price")
            @self.namespace.param("max_price", "Maximum price")
            @self.namespace.param("min_rating", "Minimum rating")
            @self.namespace.param("max_rating", "Maximum rating")
            @self.namespace.response(200, f"{entity_name} retrieved")
            @self.namespace.response(404, f"{entity_name} not found")
            @self.namespace.response(401, "Unauthorized")
            @jwt_required()
            def get(self):
                name = request.args.get("name")
                category = request.args.get("category")
                min_price = request.args.get("min_price", type=float)
                max_price = request.args.get("max_price", type=float)
                min_rating = request.args.get("min_rating", type=int)
                max_rating = request.args.get("max_rating", type=int)

                # Tạo dict chứa các tham số lọc
                filters = {
                    "name": name,
                    "category": category,
                    "min_price": min_price,
                    "max_price": max_price,
                    "min_rating": min_rating,
                    "max_rating": max_rating
                }

                # Loại bỏ các tham số có giá trị None
                filters = {k: v for k, v in filters.items() if v is not None}
                # Lấy tham số từ query
                session = container.usecase.get_session_manager()
                query = session.query(
                    Product,
                    func.avg(Feedback.star).label('avg_rating')
                ).outerjoin(Feedback).group_by(Product._id)

                if "name" in filters:
                    query = query.filter(Product.name.ilike(f"%{filters['name']}%"))
                if "category" in filters:
                    query = query.filter(Product.category_id == filters["category"])
                if "min_price" in filters:
                    query = query.filter(Product.price >= filters["min_price"])
                if "max_price" in filters:
                    query = query.filter(Product.price <= filters["max_price"])
                if "min_rating" in filters:
                    query = query.having(func.avg(Feedback.star) >= filters["min_rating"])
                if "max_rating" in filters:
                    query = query.having(func.avg(Feedback.star) <= filters["max_rating"])

                list_data = query.all()

                if list_data:
                    # Serialize results, taking only Product part from each tuple in list_data
                    results = schema.dump([product for product, _ in list_data], many=True)
                    return results, 200
                else:
                    return {"error": f"{entity_name} not found"}, 404
