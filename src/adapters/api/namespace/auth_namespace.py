from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity
)
from flask_restx import Api, Resource
from sqlalchemy import Row

from src.containers.role_container import RoleContainer
from src.domain.entities.utils import get_new_uuid, obj_to_dict
from src.containers.user_profile_container import UserProfileContainer
from werkzeug.security import generate_password_hash, check_password_hash

from src.domain.entities.user_profile import UserProfile
from src.domain.schemas.user_profile_schema import UserProfileSchema

class AuthNamespace:
    def __init__(
        self,
        container: UserProfileContainer,
        role_container: RoleContainer,
        schema: UserProfileSchema,
        api: Api,
        namespace_name: str,
    ):
        self.api = api
        self.namespace_name = namespace_name
        namespace = api.namespace(
            namespace_name
        )

        @namespace.route("/login")
        class Login(Resource):
            def post(self):
                data = request.get_json()
                user_name = data.get("username")
                password = data.get("password")
                user = dict(container.usecase.find_by_query({"username": user_name})[0]._mapping)
                if user and (check_password_hash(password=password, pwhash=user['password'])):
                    access_token = create_access_token(identity=user_name)
                    refresh_token = create_refresh_token(identity=user_name)
                    return {
                            "data": schema.dump(user),
                            "message": "Logged In ",
                            "tokens": {"access": access_token, "refresh": refresh_token},
                        }, 200
                return {"error": "Invalid username or password"}, 400          

        @namespace.route("/admin_login")
        class AdminLogin(Resource):
            def post(self):
                data = request.get_json()
                user_name = data.get("username")
                password = data.get("password")
                user = dict(container.usecase.find_by_query({"username": user_name})[0]._mapping)
                if user and (check_password_hash(password=password, pwhash=user['password'])):
                    role = role_container.usecase.find_by_id(user['role_id'])
                    if role['name'] == 'Admin':
                        access_token = create_access_token(identity=user_name)
                        refresh_token = create_refresh_token(identity=user_name)
                        return {
                                "data": schema.dump(user),
                                "message": "Logged In ",
                                "tokens": {"access": access_token, "refresh": refresh_token},
                            }, 200
                return {"error": "Invalid username or password"}, 400      
        
        @namespace.route("/register")
        class Register(Resource):
            def post(self):
                data = request.get_json()
                print(data)
                user_name = data.get("username")
                password = data.get("password")
                data['_id'] = get_new_uuid()
                user =  container.usecase.find_by_query({"username": user_name})
                print(len(user))
                if len(user) != 0:
                    print("User already exists")
                    return {"error": "User already exists"}, 409
                print(data)
                new_user = UserProfile(**data)
                print(str(new_user))
                new_user.password = generate_password_hash(password)
                temp = schema.dump(new_user)
                print(temp)
                print(type(temp))
                container.usecase.insert(schema.dump(new_user))
                return {"message": "User registered successfully"}, 201
            
        @namespace.route("/refresh")
        class Refresh(Resource):
            @jwt_required(refresh=True)
            def get(self):
                identity = get_jwt_identity()
                new_access_token = create_access_token(identity=identity)
                return {"access_token": new_access_token}, 200