from loguru import logger

from sqlalchemy.exc import SQLAlchemyError

from blog.models import Category
from blog.models import Comment
from blog.models import Post


def get_statistic():
    """Метод получения статистики постов из БД.

    Возвращает словарь из двух элементов: количество постов и количество черновиков.

    {
    'categories_count':      int,
    'comment_count':         int,
    'draft_count':           int,
    'post_count':            int,
    'total_in_posts_table':  int
    }

    В случае возникновения ошибки при обращении к БД - вмето значения,
    которое не удалось получить подставляется None значение.

    При невозможности смены тэга происходит raise Exceptions
    с сообщением соответствующим причине ошибки.

    """

    statistic = {'categories_count': None,
                 'comment_count': None,
                 'draft_count': None,
                 'post_count': None,
                 'total_in_posts_table': None}

    try:
        post_count = Post.query.filter(Post.is_draft == False).count()
        statistic['post_count'] = post_count

        draft_count = Post.query.filter(Post.is_draft == True).count()
        statistic['draft_count'] = draft_count

        statistic['total_in_posts_table'] = post_count + draft_count

        categories_count = Category.query.count()
        statistic['categories_count'] = categories_count

        comment_count = Comment.query.count()
        statistic['comment_count'] = comment_count

    except SQLAlchemyError as e:
        logger.warning(f'Не удалось получить статистику. Причина: {str(e)}')
        raise Exception('БД временно недоступна')

    return statistic

