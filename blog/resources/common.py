from flask import jsonify


def make_exception_response(exception_massage: str):
    """Вспомогательный метод создания response.

    Принимает сообщение исключения.
    Возвращает response, содержащий JSON:

    'status': str  -  текст исключения

    В зависимости от текста - добавляется подходящий код статуса.

    Возможные коды ошибок:
    При ошибке обращения - 409
    При невозможности подключения к БД - 503

    """

    response = jsonify({'status': exception_massage})

    if 'БД временно недоступна' in exception_massage:
        response.status_code = 503
    else:
        response.status_code = 409

    return response

