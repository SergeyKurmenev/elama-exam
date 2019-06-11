from flask import jsonify
from flask import Response

from flask_restful import Resource
from flask_restful import reqparse

from flask_restful_swagger import swagger

from blog.db_utils.comments import add_comment
from blog.db_utils.comments import get_all_comments_for_post

from blog.resources.common import make_exception_response


class Comments(Resource):
    """Класс для работы с комментариями."""

    @swagger.operation(
        parameters=[
            {
                "name": "post_id",
                "description": "Id поста для которого создаётся комментарий",
                "in": "query",
                "dataType": "integer",
                "paramType": "form"
            },
            {
                "name": "email",
                "description": "Email оставляющего комментарий",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "name",
                "description": "Имя оставляющего комментарий",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "text",
                "description": "Текст комментария",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            }
        ],
        responseMessages=[
            {
                "code": 409,
                "message": "Конфликт при попытке создания"
                           "(текст зависит от конкретной причины - "
                           "не найден пост/присланы не корректные данные)"
            },
            {
                "code": 503,
                "message": "БД временно недоступна"
            }
        ]
    )
    def post(self):
        """POST запрос для добавления комментария к посту.

        Принимает JSON с информацие для создания коммента.

        {
        'post_id':  int,
        'email':    str,
        'name':     str,
        'text':     str
        }

        post_id - id поста для которого создаётся комментарий
        email - email оставляющего комментарий
        name - имя оставляющего комментарий
        body - текс комментария

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
        parser.add_argument('post_id')
        parser.add_argument('email')
        parser.add_argument('name')
        parser.add_argument('text')

        args = parser.parse_args()

        try:
            add_comment(post_id=args['post_id'],
                        email=args['email'],
                        name=args['name'],
                        body=args['text'])

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return Response(status=201)

    @swagger.operation(
        parameters=[
            {
                "name": "post_id",
                "description": "Id поста для которого необходимо получить комментарии",
                "in": "query",
                "dataType": "integer",
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 409,
                "message": "Не удалось получить комментарии адресованные посту."
                           "Причина: пост с id {post_id} не найден."
            },
            {
                "code": 503,
                "message": "БД временно недоступна"
            }
        ]
    )
    def get(self):
        """GET запрос для получения всех комментариев поста.

        Принимает JSON с id поста для которого
        необходимо найти комментарии.

        {
        'post_id':  int
        }

        Возвращает JSON объект содержащий все комментарии из БД,
        которые адресованы посту с id из запроса.
        Каждый комментарий имеет вид определённый в методе `to_dict`
        класса `Comment` в blog/models.py.

        {
        'id':       int,
        'post_id':  int,
        'email':    str,
        'name':     str,
        'body':     str
        }

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON и соответствующий код:

        {
        'status': str
        }

        Status code:

        При невозможности подключения к БД - 503
        При отсутствии поста, для которого необходимо получить комментарии - 409

        """

        parser = reqparse.RequestParser()
        parser.add_argument('post_id')
        args = parser.parse_args()

        post_id = args['post_id']

        try:
            comments = get_all_comments_for_post(post_id=post_id)

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        result = []
        for comment in comments:
            result.append(comment.to_dict())

        return jsonify(result)

