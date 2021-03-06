from loguru import logger

from sqlalchemy.exc import DataError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm.exc import NoResultFound

from blog import db

from blog.models import Comment
from blog.models import Post


def add_comment(post_id: int, email: str, name: str, body: str):
    """Метод добавления комментария.

    В качестве входных параметров принимает:

    post_id:   int  -   id поста к которому создаётся комментарий
    email:     str  -   email оставившего комментарий
    name:      str  -   имя оставившего комментарий
    body:      str  -   текст комментария

    Перед попыткой создать комментарий - происходит проверка существования
    поста которому он адресован.

    В случае провала проверки существования поста или
    возникновении ошибки при попытке создания комментария происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:

        # Проверка существования поста для которого добавляется комментарий
        if not Post.query.filter(Post.id == post_id).count():
            raise NoResultFound('Пост не найден.')

        comment_for_add = Comment(post_id=post_id,
                                  email=email,
                                  name=name,
                                  body=body)

        db.session.add(comment_for_add)
        db.session.commit()

    except DataError as e:
        logger.warning('Не удалось создать комментарий. '
                       f'Причина: {str(e)}.')
        raise Exception('Не удалось создать комментарий. '
                        'Причина: не корректный id поста.')

    except NoResultFound:
        warning_massage = 'Не удалось создать комментарий. ' \
                          f'Причина: пост с id: {post_id} не найден.'
        logger.warning(warning_massage)
        raise Exception(warning_massage)

    except IntegrityError as e:
        db.session.rollback()
        logger.warning('Не удалось создать новый комментарий. '
                       f'Причина: {str(e)}')
        raise Exception('Не удалось создать новый комментарий. '
                        'Проверьте корректность данных.')

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.warning('Не удалось создать новый комментарий. '
                       f'Причина: {str(e)}')
        raise Exception('БД временно недоступна')


def get_all_comments_for_post(post_id: int):
    """Метод получения всех комментариев, адресованных определённому посту.

    В качестве входных параметров принимает:

    post_id:  int  -  id поста, для которого необходимо найти все комментарии.

    Возвращает список всех комментариев(список объектов Comment) поста.
    [
        {
        id:       int,
        post_id:  int,
        email:    str,
        name:     str,
        body:     str
        },
        ... ,
        {}
    ]

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:
        # Проверка существования поста для которого необходимо получить комментарии
        if not Post.query.filter(Post.id == post_id).count():
            raise NoResultFound('Пост не найден')

        comments = Comment.query.filter(Comment.post_id == post_id).all()

    except DataError as e:
        logger.warning(f'Не удалось получить комментарии адресованные посту с id: {post_id}. '
                       f'Причина: {str(e)}.')
        raise Exception('Не удалось получить комментарии адресованные посту. '
                        f'Причина: Не корректный id - {post_id}.')

    except NoResultFound as e:
        logger.warning(f'Не удалось получить комментарии адресованные посту с id: {post_id}. '
                       f'Причина: {str(e)}.')
        raise Exception('Не удалось получить комментарии адресованные посту. '
                        f'Причина: пост с id {post_id} не найден.')

    except SQLAlchemyError as e:
        logger.warning(f'Не удалось получить комментарии адресованные посту с id: {post_id}. '
                       f'Причина: {str(e)}.')
        raise Exception('БД временно недоступна')

    return comments

