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
        постов и черновиков в БД:

        'categories_count':      int  -  количество категорий
        'comment_count':         int  -  количество комментариев
        'draft_count':           int  -  количество черновиков
        'post_count':            int  -  количество постов
        'total_in_posts_table':  int  -  количество постов + черновиков

        В случае ошибки возвращает сообщение соответствующее
        типу ошибки в виде JSON(в поле 'status' находится сообщение ошибки)
        и соответствующий код.

        Возможные коды ошибок:
        При невозможности подключения к БД - 503

        """

        try:
            statistic = get_statistic()
        except Exception as e:
            response = make_exception_response(str(e))
            return response

        return jsonify(statistic)

