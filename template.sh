#!/bin/bash
object_name=$1
option=$2


help_txt="""
Usage: bash setup/template.sh <object_name> <option>
Options:
    -c: Create object
    -d: Delete object
exp:
    bash setup/template.sh user_data -c
    bash setup/template.sh user_file -d
"""
if [ -z "$object_name" ]; then
    echo "$help_txt"
    exit 1
fi

if [ -z "$option" ]; then
    echo "$help_txt"
    exit 1
fi

object_name_upper=$(echo $object_name | sed -r "s/(^|_)([a-z])/\U\2/g")

if [ "$option" == "-c" ]; then
    echo "Tạo các tệp cho $object_name_upper"
    read -p "Có tiếp tục không? (bấm Enter để tiếp tục, bất kỳ phím nào khác để dừng)?: " user_input

    if [[ -n $user_input ]]; then
        echo "Dừng lại."
        exit 1
    else
        echo "Tiếp tục..."
        # Thực hiện các hành động tiếp theo
    fi
    # tạo entity
    touch  src/domain/entities/${object_name}.py
    echo "Created  src/domain/entities/${object_name}.py"

    echo "
from src.domain.entities.entity import Entity

class ${object_name_upper}(Entity):
    __tablename__ = '${object_name}'
    def __init__(self, _id: str):
        super().__init__(_id)
    " >>  src/domain/entities/${object_name}.py

    # tạo usecase
    touch  src/usecases/${object_name}_usecase.py
    echo "Created  src/usecases/${object_name}_usecase.py"
    echo "
from src.usecases.entity_usecase import EntityUsecase
from src.domain.services.${object_name}_service import ${object_name_upper}Service

class ${object_name_upper}Usecase(EntityUsecase):
    def __init__(self, ${object_name}_service: ${object_name_upper}Service):
        super().__init__(${object_name}_service)
    " >>  src/usecases/${object_name}_usecase.py

    # tạo schema
    touch  src/domain/schemas/${object_name}_schema.py
    echo "Created  src/domain/schemas/${object_name}_schema.py"

    echo "
from marshmallow import Schema, fields

class ${object_name_upper}Schema(Schema):
    _id = fields.Str(required=True, metadata={"description": "Category ID"})

    " >>  src/domain/schemas/${object_name}_schema.py


    # tạo service
    touch  src/domain/services/${object_name}_service.py
    echo "Created  src/domain/services/${object_name}_service.py"

    echo "
from src.adapters.services.entity_service_impl import EntityServiceImpl
from src.adapters.repositories.${object_name}_repository import ${object_name_upper}Repository


class ${object_name_upper}Service(EntityServiceImpl):
    def __init__(self, ${object_name}_repository: ${object_name_upper}Repository):
        super().__init__(${object_name}_repository)

    " >>  src/domain/services/${object_name}_service.py



    #  tạo repository
    touch  src/adapters/repositories/${object_name}_repository.py
    echo "Created  src/adapters/repositories/${object_name}_repository.py"

    echo "
from src.adapters.repositories.entity_repository import EntityRepository
from pymongo.collection import Collection

class ${object_name_upper}Repository(EntityRepository):
    def __init__(self, collection: Collection):
        self.collection = collection
    " >>  src/adapters/repositories/${object_name}_repository.py




    # tạo service_impl
    touch  src/adapters/services/${object_name}_service_impl.py
    echo "Created  src/adapters/services/${object_name}_service_impl.py"

    echo "
from src.adapters.repositories.${object_name}_repository import ${object_name_upper}Repository
from src.domain.services.${object_name}_service import ${object_name_upper}Service


class ${object_name_upper}ServiceImpl(${object_name_upper}Service):
    pass

    " >>  src/adapters/services/${object_name}_service_impl.py  


    # tạo container
    touch  src/containers/${object_name}_container.py
    echo "Created  src/containers/${object_name}_container.py"

    echo "
from src.containers.repository_container import RepositoryContainer
from src.adapters.services.${object_name}_service_impl import ${object_name_upper}ServiceImpl
from src.usecases.${object_name}_usecase import ${object_name_upper}Usecase

class ${object_name_upper}Container:
    def __init__(self, repository_container: RepositoryContainer):
        service = ${object_name_upper}ServiceImpl(repository_container.${object_name}_repository)
        self.usecase = ${object_name_upper}Usecase(service)

    " >>  src/containers/${object_name}_container.py


    # Tạo namespace
    touch src/adapters/api/namespace/${object_name}_namespace.py
    echo "Create src/adapters/api/namespace/${object_name}_namespace.py"
    cat << EOF >> src/adapters/api/namespace/${object_name}_namespace.py
from flask_restx import Api
from src.containers.${object_name}_container import ${object_name_upper}Container
from src.domain.schemas.${object_name}_schema import ${object_name_upper}Schema
from src.adapters.api.namespace.entity_namespace import EntityNamespace

class ${object_name_upper}Namespace(EntityNamespace):
    def __init__(
        self,
        container: ${object_name_upper}Container,
        schema: ${object_name_upper}Schema,
        api: Api,
        namespace_name: str,
        entity_name: str):
        super().__init__(container, schema, api, namespace_name, entity_name)

EOF


    # tạo test api
    touch tests/apis/test_${object_name}.py
    echo "Created tests/apis/test_${object_name}.py"


cat << EOF >> tests/apis/test_${object_name}.py 
import os
from src.domain.entities.utils import get_current_timestamp_str
from src.domain.entities.cost import *
from src.domain.schemas.entity_schema import EntitySchema
from src.containers.${object_name}_container import ${object_name_upper}Container
import requests
import pytest

@pytest.fixture(scope="module")
def host():
    return os.getenv("APP_HOST")


@pytest.fixture(scope="module")
def endpoint(host):
    return f"{host}/api/v1/${object_name}/"


def test_${object_name}_api(host, endpoint):
    headers = {"Content-Type": "application/json"}
    _id = "1"

    data = {"_id": _id, "created_at": get_current_timestamp_str()}
EOF



    # tạo test container
    touch tests/containers/test_${object_name}_container.py
    echo "Created tests/containers/test_${object_name}_container.py"

cat << EOF >> tests/containers/test_${object_name}_container.py 
from src.containers.repository_container import RepositoryContainer
from src.domain.entities.utils import get_current_timestamp_str
from src.domain.schemas.${object_name}_schema import ${object_name_upper}Schema
from src.containers.${object_name}_container import ${object_name_upper}Container

def test_${object_name}_container():
    ${object_name}_container = ${object_name_upper}Container(RepositoryContainer())

    assert ${object_name}_container.usecase is not None
EOF

    echo "Create $object_name_upper done"


    # tạo test repository
    mkdir -p tests/repositories
    touch tests/repositories/test_${object_name}_repository.py
    echo "Created tests/repositories/test_${object_name}_repository.py"

    cat << EOF >> tests/repositories/test_${object_name}_repository.py 
from src.domain.entities.utils import get_current_timestamp_str
from src.domain.schemas.${object_name}_schema import ${object_name_upper}Schema
from src.adapters.repositories.${object_name}_repository import ${object_name_upper}Repository

def test_${object_name}_repository():
    ${object_name}_repository = ${object_name_upper}Repository()
    assert ${object_name}_repository is not None
EOF
    exit 0
fi
if [ "$option" == "-d" ]; then

    echo "Delete $object_name_upper"
    read -p "Có tiếp tục không? (bấm Enter để tiếp tục, bất kỳ phím nào khác để dừng)?: " user_input

    if [[ -n $user_input ]]; then
        echo "Dừng lại."
        exit 1
    else
        echo "Tiếp tục..."
        # Thực hiện các hành động tiếp theo
        echo "Delete $object_name_upper"
        rm -rf src/domain/entities/${object_name}.py
        echo "Delete src/domain/entities/${object_name}.py"
        rm -rf src/usecases/${object_name}_usecase.py
        echo "Delete src/usecases/${object_name}_usecase.py"
        rm -rf src/domain/schemas/${object_name}_schema.py
        echo "Delete src/domain/schemas/${object_name}_schema.py"
        rm -rf src/domain/services/${object_name}_service.py
        echo "Delete src/domain/services/${object_name}_service.py"
        rm -rf src/adapters/repositories/${object_name}_repository.py
        echo "Delete src/adapters/repositories/${object_name}_repository.py"
        rm -rf src/adapters/services/${object_name}_service_impl.py
        echo "Delete src/adapters/services/${object_name}_service_impl.py"
        rm -rf src/containers/${object_name}_container.py
        echo "Delete src/containers/${object_name}_container.py"
        rm -rf src/adapters/api/resources/${object_name}_resource.py
        echo "Delete src/adapters/api/resources/${object_name}_resource.py"
        rm -rf tests/apis/test_${object_name}.py
        echo "Delete tests/apis/test_${object_name}.py"
        rm -rf tests/containers/test_${object_name}_container.py
        echo "Delete tests/containers/test_${object_name}_container.py"

        rm -rf tests/repositories/test_${object_name}_repository.py
        echo "Delete tests/repositories/test_${object_name}_repository.py"

        echo "Delete $object_name_upper done"
    fi
    exit 0
fi

