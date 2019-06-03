from flask import jsonify
from flask import Response

from flask_restful import Resource
from flask_restful import reqparse

from blog import api

from blog.db_utils.posts import add_post
from blog.db_utils.posts import change_post_tag
from blog.db_utils.posts import get_all_posts
from blog.db_utils.posts import get_statistic


class Posts(Resource):
    """Класс для работы с постами."""

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

        """
        posts = get_all_posts()
        result = []
        for post in posts:
            result.append(post.to_dict())
        return jsonify(result)

    def post(self):
        """POST запрос для добавления поста/черновика.

        Принимает JSON с информацией для создания поста.

        {
        'user_id':  str,
        'title':    str,
        'body':     str,
        'is_draft': str,
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

        """

        parser = reqparse.RequestParser()
        parser.add_argument('user_id')
        parser.add_argument('title')
        parser.add_argument('body')
        parser.add_argument('is_draft')
        parser.add_argument('tag')

        args = parser.parse_args()

        add_post(user_id=int(args['user_id']),
                 title=args['title'],
                 body=args['body'],
                 is_draft=bool(args['is_draft']),
                 tag=args['tag'])

        return Response(status=200)

    def put(self):
        """PUT метод для добавления/редактирования тэга поста.

        Принимает JSON с информацией для замены тэга.

        {
        'post_id': str,
        'tag':     str
        }

        post_id - id поста для которого будет происходить смена тэга
        tag - новый тэг поста(при отсутствии - будет записано null значение)

        """

        parser = reqparse.RequestParser()
        parser.add_argument('post_id')
        parser.add_argument('tag')

        args = parser.parse_args()

        change_post_tag(post_id=int(args['post_id']),
                        tag=args['tag'])

        return Response(status=200)


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


api.add_resource(Posts, '/api/v1/posts')
api.add_resource(Statistic, '/api/v1/statistic')

