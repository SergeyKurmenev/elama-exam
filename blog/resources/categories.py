from flask import jsonify
from flask import Response

from flask_restful import Resource
from flask_restful import reqparse

from flask_restful_swagger import swagger

from blog.db_utils.categories import add_category
from blog.db_utils.categories import change_category
from blog.db_utils.categories import delete_category
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
        ],
        responseMessages=[
            {
                "code": 409,
                "message": "Не корректные данные, возможно такая категория или тэг уже заняты"
            },
            {
                "code": 503,
                "message": "БД временно недоступна"
            }
        ]
    )
    def post(self):
        """POST запрос для создания категории.

        Принимает JSON с информацией для создания категории:

        'name':   str  -  название категории
        'tag':    str  -  тэг категории

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON(в поле 'status' находится сообщение ошибки)
        и соответствующий код.

        Возможные коды ошибок:
        При ошибке записи - 409
        При невозможности подключения к БД - 503

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
        ],
        responseMessages=[
            {
                "code": 409,
                "message": "Конфликт при попытке редактирования"
                           "(текст зависит от конкретной причины - "
                           "не найдена категория/новое имя или тэг уже заняты)"
            },
            {
                "code": 503,
                "message": "БД временно недоступна"
            }
        ]
    )
    def put(self):
        """PUT запрос для изменения категории.

        Принимает JSON с информацией для изменения категории:

        'category_id':  int  -  id категории, которую необходимо изменить
        'name':         str  -  опциональный параметр - новое название категории
        'tag':          str  -  опциональный параметр - новый тэг категории

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON(в поле 'status' находится сообщение ошибки)
        и соответствующий код.

        Возможные коды ошибок:
        При ошибке записи - 409
        При невозможности подключения к БД - 503

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

    @swagger.operation(
        responseMessages=[
            {
                "code": 503,
                "message": "БД временно недоступна"
            }
        ]
    )
    def get(self):
        """GET запрос для получения всех существующих категорий.

        Возвращает JSON объект содержащий все категории из БД.
        Каждая категория имеет вид определённый в методе `to_dict`
        класса `Category` в blog/models.py:

        'id':    int  -  id категории
        'name':  str  -  название категории
        'tag':   str  -  тэг категории

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON(в поле 'status' находится сообщение ошибки)
        и соответствующий код.

        Возможные коды ошибок:
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

    @swagger.operation(
        parameters=[
            {
                "name": "category_id",
                "description": "Id удаляемой категории",
                "in": "query",
                "dataType": "integer",
                "paramType": "form"
            }
        ],
        responseMessages=[
            {
                "code": 409,
                "message": "Проверьте корректость id удаляемой категории."
            },
            {
                "code": 503,
                "message": "БД временно недоступна"
            }
        ]
    )
    def delete(self):
        """DELETE запрос для удаления категории.

        Принимает JSON с id категории которую необходимо удалить:

        'category_id':  int  -  id удаляемой категории

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON(в поле 'status' находится сообщение ошибки)
        и соответствующий код.

        Возможные коды ошибок:
        При отсутствии удаляемой категории - 409
        При невозможности подключения к БД - 503

        """

        parser = reqparse.RequestParser()
        parser.add_argument('category_id')
        args = parser.parse_args()

        try:
            delete_category(category_id=args['category_id'])
        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return Response(status=200)

