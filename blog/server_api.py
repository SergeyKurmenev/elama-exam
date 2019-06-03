from flask import jsonify

from flask_restful import Resource

from blog import api

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

