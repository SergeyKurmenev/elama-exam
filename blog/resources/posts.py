from flask import jsonify
from flask import Response

from flask_restful import Resource
from flask_restful import reqparse

from flask_restful_swagger import swagger

from blog.db_utils.posts import add_post
from blog.db_utils.posts import change_post_tag
from blog.db_utils.posts import delete_posts
from blog.db_utils.posts import get_all_posts

from blog.resources.common import make_exception_response


class Posts(Resource):
    """Класс для работы с постами."""

    @swagger.operation()
    def get(self):
        """GET запрос для получения всех постов.

        Возвращает JSON объект содержащий все посты из БД.
        Каждый пост имеет вид определённый в методе `to_dict`
        класса `Post` в blog/models.py.

        {
        'id':       int,
        'user_id':  int,
        'title':    str,
        'body':     str,
        'tag':      str
        }

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON и соответствующий код:

        {
        'status': str
        }

        Status code:

        При невозможности подключения к БД - 503

        """

        try:
            posts = get_all_posts()

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        result = []
        for post in posts:
            result.append(post.to_dict())
        return jsonify(result)

    @swagger.operation(
        parameters=[
            {
                "name": "user_id",
                "description": "Id пользователя создающего пост",
                "in": "query",
                "dataType": "integer",
                "paramType": "form"
            },
            {
                "name": "title",
                "description": "Заголовок поста",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "text",
                "description": "Текст поста",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            },
            {
                "name": "is_draft",
                "description": "Пометка 'черновик'(опционально, boolean значение)",
                "in": "query",
                "dataType": "boolean",
                "paramType": "form"
            },
            {
                "name": "tag",
                "description": "Тэг поста (опционально)",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            },
        ]
    )
    def post(self):
        """POST запрос для добавления поста/черновика.

        Принимает JSON с информацией для создания поста.

        {
        'user_id':  int,
        'title':    str,
        'text':     str,
        'is_draft': bool,
        'tag':      str
        }

        user_id - id пользователя, размещающего пост
        title - заголовок поста
        body - текс поста
        is_draft - опциональный параметр для сохранения поста в качестве черновика
            при значении False или отсутствии - сохраняется как пост
            при значении True - сохраненяется как черновик
        tag - опциональный параметр для добавления тэга к посту
            при отсутствии - будет сохранено null значение

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
        parser.add_argument('user_id')
        parser.add_argument('title')
        parser.add_argument('text')
        parser.add_argument('is_draft')
        parser.add_argument('tag')

        args = parser.parse_args()

        is_draft = False

        # Проверка входящего значения is_draft(пометка "черновик")
        # для корректной обработки строк.
        if args['is_draft'] and args['is_draft'].lower() == 'true':
            is_draft = True

        try:
            add_post(user_id=args['user_id'],
                     title=args['title'],
                     body=args['text'],
                     is_draft=is_draft,
                     tag=args['tag'])

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return Response(status=201)

    @swagger.operation(
        parameters=[
            {
                "name": "post_id",
                "description": "Id поста которому необходимо сменить тэг",
                "in": "query",
                "dataType": "integer",
                "paramType": "form"
            },
            {
                "name": "tag",
                "description": "Новый тэг поста(должна существовать категория с данным тэгом)",
                "in": "query",
                "dataType": "string",
                "paramType": "form"
            }
        ]
    )
    def put(self):
        """PUT запрос для добавления/редактирования тэга поста.

        Принимает JSON с информацией для замены тэга.

        {
        'post_id': int,
        'tag':     str
        }

        post_id - id поста для которого будет происходить смена тэга
        tag - новый тэг поста(при отсутствии - будет записано null значение)

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
        parser.add_argument('tag')

        args = parser.parse_args()

        try:
            change_post_tag(post_id=args['post_id'],
                            tag=args['tag'])

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return Response(status=201)

    @swagger.operation(
        parameters=[
            {
                "name": "posts_id",
                "description": "Id удаляемого поста(при удалении нескольких - id печисляются через ',')",
                "in": "query",
                "dataType": "integer",
                "paramType": "form"
            }
        ]
    )
    def delete(self):
        """DELETE запрос для удаления постов.

        Принимает JSON с id постов, которые необходимо удалить.

        {
        'posts_id':  int
        }

        posts_id - id постов для удаления.
            Возможно удаление одного или нескольких постов.
            Для удаления нескольких постов - в posts_id необходимо
            передать строку с перечислением id постов разделённых с помощью ','.
            {
            'posts_id': '34,45,67,89,2'
            }

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON и соответствующий код:

        {
        'status': str
        }

        Status code:

        При невозможности подключения к БД - 503

        """

        parser = reqparse.RequestParser()
        parser.add_argument('posts_id')
        args = parser.parse_args()

        try:
            try:
                separated_posts_id = args['posts_id'].replace(' ', '').split(',')
            except Exception:
                raise Exception('Проверьте корректность параметра posts_id')

            delete_posts(*separated_posts_id)

        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return Response(status=200)

