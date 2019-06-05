from flask import jsonify

from flask_restful import Resource

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
            response = jsonify({'status': str(e)})
            response.status_code = 503

            return response

        return jsonify(statistic)

