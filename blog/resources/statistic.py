from flask import jsonify

from flask_restful import Resource

from flask_restful_swagger import swagger

from blog.db_utils.statistic import get_statistic

from blog.resources.common import make_exception_response


class Statistic(Resource):
    """Класс для работы со статистикой."""

    @swagger.operation(
        responseMessages=[
            {
                "code": 503,
                "message": "БД временно недоступна"
            }
        ]
    )
    def get(self):
        """GET запрос для получения статистики постов.

        Возвращает JSON объект содержащий статистику
        постов и черновиков в БД.

        Статистика возвращается в виде:

        {
        'categories_count':      int,
        'draft_count':           int,
        'post_count':            int,
        'total_in_posts_table':  int
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
            statistic = get_statistic()
        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return jsonify(statistic)

