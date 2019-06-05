from loguru import logger

from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError

from blog import db

from blog.models import Comment


def add_comment(post_id: int, email: str, name: str, body: str):
    """Метод добавления комментария.

    Входные данные метода:

    post_id - id поста к которому создаётся комментарий
    email - email оставившего комментарий
    name - имя оставившего комментарий
    body - текст комментария


    """

    comment_for_add = Comment(post_id=post_id,
                              email=email,
                              name=name,
                              body=body)

    db.session.add(comment_for_add)
    try:
        db.session.commit()
    except OperationalError as e:
        db.session.rollback()
        raise Exception(str(e))


def get_all_comments_for_post(post_id: int):
    """Метод получения всех комментариев, адресованных определённому посту.

    Входные данные метода:

    post_id - id поста, для которого необходимо найти все комментарии.

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:
        comments = Comment.query.filter(Comment.post_id == post_id).all()
    except SQLAlchemyError as e:
        logger.warning('Не удалось получить комментарии адресованные посту с id: {}. '
                       'Причина: {}.'.format(post_id, str(e)))
        raise Exception('БД временно недоступна')

    return comments

