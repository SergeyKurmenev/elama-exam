from flask import jsonify
from flask import Response

from flask_restful import Resource
from flask_restful import reqparse

from flask_restful_swagger import swagger

from blog.db_utils.categories import change_category
from blog.db_utils.categories import add_category
from blog.db_utils.categories import get_all_categories

from blog.resources.common import make_exception_response


class Categories(Resource):
    """Класс для работы с категориями."""

    @swagger.operation(
        parameters=[
            {
                "name": "name",
                "description": "Название категории",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "tag",
                "description": "Тэг категории",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            }
        ]
    )
    def post(self):
        """POST запрос для создания категории.

        Принимает JSON с информацией для создания категории.

        {
        'name':   str,
        'tag':    str
        }

        name - название категории
        tag - тэг, который будет использоваться для
        причисления поста к данной категории

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON и соответствующий код:

        {
        'status': str
        }

        Status code:

        При невозможности подключения к БД - 503
        При ошибке записи - 409
        При успешной записи - 201

        """

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('tag')
        args = parser.parse_args()

        try:
            add_category(name=args['name'],
                         tag=args['tag'])

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return Response(status=201)

    @swagger.operation(
        parameters=[
            {
                "name": "category_id",
                "description": "Id редактируемой категории",
                "in": "query",
                "dataType": "integer",
                "paramType": "form"
            },
            {
                "name": "name",
                "description": "Новое название категории(опционально)",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "tag",
                "description": "Новый тэг категории(опционально)",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            }
        ]
    )
    def put(self):
        """PUT запрос для изменения категории.

        Принимает JSON с информацией для изменения категории.

        {
        'category_id':  int,
        'name':         str,
        'tag':          str
        }

        category_id - id категории, которые необходимо изменить
        name - опциональный параметр - новое название категории
        tag - опциональный параметр - новый тэг категории

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON и соответствующий код:

        {
        'status': str
        }

        Status code:

        При невозможности подключения к БД - 503
        При ошибке записи - 409
        При успешной записи - 201

        """

        parser = reqparse.RequestParser()
        parser.add_argument('category_id')
        parser.add_argument('name')
        parser.add_argument('tag')
        args = parser.parse_args()

        try:

            change_category(category_id=args['category_id'],
                            name=args['name'],
                            tag=args['tag'])

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return Response(status=201)

    @swagger.operation()
    def get(self):
        """GET запрос для получения всех существующих категорий.

        Возвращает JSON объект содержащий все категории из БД.
        Каждая категория имеет вид определённый в методе `to_dict`
        класса `Category` в blog/models.py.

        {
        'id':    int,
        'name':  str,
        'tag':   str
        }

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON и соответствующий код:

        {
        'status': str
        }

        Status code:

        При невозможности подключения к БД - 503

        """

        result = []

        try:
            categories = get_all_categories()

            for category in categories:
                result.append(category.to_dict())

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return jsonify(result)

