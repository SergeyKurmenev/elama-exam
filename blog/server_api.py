from flask import jsonify
from flask import Response

from flask_restful import Resource
from flask_restful import reqparse

from blog import api

from blog.db_utils.categories import change_category
from blog.db_utils.categories import add_category
from blog.db_utils.categories import get_all_categories

from blog.db_utils.comments import add_comment
from blog.db_utils.comments import get_all_comments_for_post

from blog.db_utils.posts import get_statistic


class Statistic(Resource):
    """Класс для работы со статистикой."""

    def get(self):
        """GET запрос для получения статистики постов.

        Возвращает JSON объект содержащий статистику
        постов и черновиков в БД.

        Статистика возвращается в виде:

        {
        'draft_count': int,
        'post_count':  int
        }

        """
        statistic = get_statistic()
        return jsonify(statistic)


class Comments(Resource):
    """Класс для работы с комментариями."""

    def post(self):
        """POST запрос для добавления комментария к посту.

        Принимает JSON с информацие для создания коммента.

        {
        'post_id':  int,
        'email':    str,
        'name':     str,
        'body':     str
        }

        post_id - id поста для которого создаётся комментарий
        email - email оставляющего комментарий
        name - имя оставляющего комментарий
        body - текс комментария

        """

        parser = reqparse.RequestParser()
        parser.add_argument('post_id')
        parser.add_argument('email')
        parser.add_argument('name')
        parser.add_argument('body')

        args = parser.parse_args()

        add_comment(post_id=int(args['post_id']),
                    email=args['email'],
                    name=args['name'],
                    body=args['body'])

        return Response(status=200)

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

        """

        parser = reqparse.RequestParser()
        parser.add_argument('post_id')
        args = parser.parse_args()

        post_id = args['post_id']

        comments = get_all_comments_for_post(post_id=post_id)
        result = []
        for comment in comments:
            result.append(comment.to_dict())

        return jsonify(result)


class Categories(Resource):
    """Класс для работы с категориями."""

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

        """

        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('tag')
        args = parser.parse_args()

        add_category(name=args['name'],
                     tag=args['tag'])

        return Response(status=200)

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

        """

        parser = reqparse.RequestParser()
        parser.add_argument('category_id')
        parser.add_argument('name')
        parser.add_argument('tag')
        args = parser.parse_args()

        change_category(category_id=args['category_id'],
                        name=args['name'],
                        tag=args['tag'])

        return Response(status=200)

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

        """

        categories = get_all_categories()
        result = []
        for category in categories:
            result.append(category.to_dict())

        return jsonify(result)


api.add_resource(Categories, '/api/v1/categories')
api.add_resource(Comments, '/api/v1/comments')
api.add_resource(Statistic, '/api/v1/statistic')

