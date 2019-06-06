from flask import jsonify


def make_exception_response(exception_massage: str):
    """Метод создания response.

    Принимает сообщение исключения.
    Возвращает response, содержащий JSON:

    {
    'status': текст исключения
    }

    В зависимости от текста - добавляется подходящий код статуса.

    """

    response = jsonify({'status': exception_massage})

    if 'БД временно недоступна' in exception_massage:
        response.status_code = 503
    else:
        response.status_code = 409

    return response

