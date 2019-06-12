from loguru import logger

from sqlalchemy.exc import SQLAlchemyError

from blog.models import Post


def get_statistic():
    """Метод получения статистики постов из БД.

    Возвращает словарь из двух элементов: количество постов и количество черновиков.

    {
    post_count:  int,
    draft_count: int
    }

    В случае возникновения ошибки при обращении к БД - вмето значения,
    которое не удалось получить подставляется None значение.

    При невозможности смены тэга происходит raise Exceptions
    с сообщением соответствующим причине ошибки.

    """

    statistic = {'total': None,
                 'post_count': None,
                 'draft_count': None}

    try:
        post_count = Post.query.filter(Post.is_draft == False).count()
        statistic['post_count'] = post_count

        draft_count = Post.query.filter(Post.is_draft == True).count()
        statistic['draft_count'] = draft_count

        statistic['total'] = post_count + draft_count

    except SQLAlchemyError as e:
        logger.warning(f'Не удалось получить статистику. Причина: {str(e)}')
        raise Exception('БД временно недоступна')

    return statistic

