from loguru import logger

from sqlalchemy.exc import DataError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm.exc import NoResultFound

from blog import db

from blog.db_utils.comments import get_all_comments_for_post

from blog.models import Category
from blog.models import Post

from config import Config


def add_post(user_id: int, title: str, body: str, is_draft: bool = False, tag: str = None):
    """Метод добавления поста в БД.

    В качестве входных параметров принимает:

    user_id:   int   -  id пользователя создающего пост
    title:     str   -  заголовок поста*
    body:      str   -  текст поста**
    is_draft:  bool  -  пометка "черновик" - опционально(default=False - не черновик)
    tag:       str   -  тэг категории - опционально(default=None - без категории)

    * & ** имеют ограничения максимального количества символов,
    которые указаны в классе Config(config.py).
    Валидация данных полей происходит по средствам обработки
    исключений, возникших при попытке
    записи значения(превышающих допустимую длину) в БД.

    В случае ошибки при попытке создания поста происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:

        # Проверка существования категории с данным тэгом.
        # только в случае наличия тэга во входящих аргументах
        if tag and not Category.query.filter(Category.tag == tag).count():
            raise NoResultFound(f'Категория с тэгом {tag} не найдена')

        post_for_add = Post(user_id=user_id,
                            title=title,
                            body=body,
                            is_draft=is_draft,
                            tag=tag)

        db.session.add(post_for_add)
        db.session.commit()

    except NoResultFound as e:
        logger.warning('Не удалось создать пост с предоставленными данными. '
                       f'Причина: {str(e)}')
        raise Exception('Не корректные данные. '
                        'Категория с данным тэгом не найдена.')

    except IntegrityError as e:
        db.session.rollback()
        logger.warning('Не удалось создать пост с предоставленными данными. '
                       f'Причина: {str(e)}')
        raise Exception('Не корректные данные. '
                        'Проверьте наличие всех обязательных полей в запросе.')

    except DataError as e:
        db.session.rollback()
        logger.warning('Не удалось создать новый пост. '
                       f'Причина: {str(e)}')
        if 'StringDataRightTruncation' in str(e):
            raise Exception('Ошибка при попытке создания поста. '
                            'Проверьте количество символов в заголовке и тексте поста. '
                            'Максимально допустимое значение для заголовка - '
                            f'{Config.POST_TITLE_MAX_LENGTH} символов, '
                            f'для текста - {Config.POST_BODY_MAX_LENGTH} символов.')

        else:
            raise Exception('Проверьте корректность поля user_id.')

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.warning('Не удалось создать новый пост. '
                       f'Причина: {str(e)}')
        raise Exception('БД временно недоступна')


def get_all_posts():
    """Метод получения всех постов из БД.

    Возвращает список всех постов(список объектов Post),
    не отмеченных как "черновик".
    [
        {
        id:        int,
        user_id:   int,
        title:     str,
        body:      str,
        is_draft:  bool,
        tag:       str
        },
        ... ,
        {}
    ]

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:
        posts = Post.query.filter(Post.is_draft == False).all()
    except SQLAlchemyError as e:
        logger.warning('Ошибка при попытке получить все посты из БД. '
                       f'Причина: {str(e)}.')
        raise Exception('БД временно недоступна')

    return posts


def delete_posts(*args: int):
    """Метод удаления постов из БД.

    В качестве входных параметров принимает:

    *args:  int  -  id постов, которые необходимо удалить
                    (в качестве разделителя id использовать ',')

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:
        for post_id in args:
            try:
                post = Post.query.filter(Post.id == post_id).one()
                comments = get_all_comments_for_post(post_id)

                db.session.delete(post)
                for comment in comments:
                    db.session.delete(comment)

            except NoResultFound as e:
                logger.warning(f'Пост c id: {post_id} не удалён. '
                               f'Причина: {str(e)}')

        db.session.commit()

    except DataError as e:
        logger.warning(f'Ошибка при попытке удаления постов: {[*args]}. '
                       f'Причина: {str(e)}.')
        raise Exception('Проверьте корректность параметра posts_id')

    except SQLAlchemyError as e:
        logger.warning(f'Ошибка при попытке удаления постов: {[*args]}. '
                       f'Причина: {str(e)}.')
        raise Exception('БД временно недоступна')


def change_post_tag(post_id: int, tag: str):
    """Метод добавления/изменения тэга поста

    В качестве входных параметров принимает:

    post_id:  int  -  id поста, которому необходимо заменить тэг
    tag:      str  -  тэг(при None значении - тэг поста будет удалён)

    При невозможности смены тэга происходит raise Exceptions
    с сообщением соответствующим причине ошибки.

    """

    try:

        # Проверка на существование категории с данным тэгом
        if tag and not Category.query.filter(Category.tag == tag).count():
            raise NoResultFound(f'Категория с тэгом {tag} не найдена')

        post_for_change_tag = Post.query.filter(Post.id == post_id).one()
        post_for_change_tag.tag = tag

        db.session.commit()

    except DataError as e:
        logger.warning(f'Тэг для поста с id: {post_id}  на новый тэг "{tag}" не изменён. '
                       f'Причина: {str(e)} ')
        raise Exception('Не удалось заменить тэг поста. '
                        'Причина: не корректный id поста.')

    except NoResultFound as e:
        logger.warning(f'Тэг для поста с id: {post_id}  на новый тэг "{tag}" не изменён. '
                       f'Причина: {str(e)} ')
        raise Exception('Не удалось заменить тэг поста. '
                        'Проверьте правильность предоставленного id поста '
                        'и существование предоставленного тэга')

    except SQLAlchemyError as e:
        logger.warning(f'Тэг для поста с id: {post_id} не изменён. Причина: {str(e)}')
        raise Exception('БД временно недоступна')


def get_posts_with_tag(tag: str):
    """Вспомогательный метод получения всех постов категории.

    В качестве входного параметра принимает:

    tag:  str  -  тэг, по которому будет происходить выборка постов

    Возвращает список объектов класса Post, которые
    отмечены данным тэгом(в т.ч. и черновики).
    [
        {
        id:        int,
        user_id:   int,
        title:     str,
        body:      str,
        is_draft:  bool,
        tag:       str
        },
        ... ,
        {}
    ]

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:
        posts = Post.query.filter(Post.tag == tag).all()
    except SQLAlchemyError as e:
        logger.warning(f'Не удалось получить посты, отмеченные тэгом: {tag}. '
                       f'Причина: {str(e)}.')
        raise Exception('БД временно недоступна')

    return posts


def refresh_tag(old_tag: str, new_tag: str):
    """Вспомогательный метод для обновления тэгов в постах.

    Входные параметры метода:

    old_tag - тэг который необходимо заменить
    new_tag - тэг на который необходимо заменить
        при None значении - запись категории меняется
        на null(без категории)

    Метод используется после редактирования тэга
    какой-либо категории для обновления тэга
    в постах на актуальный.

    В случае ошибки выводит информацию о причине
    в консоль с помощью logger.

    """

    try:
        posts = get_posts_with_tag(old_tag)

        for post in posts:
            post.tag = new_tag

        db.session.commit()

    except SQLAlchemyError as e:
        logger.warning(f'Не удалось обновить тэги постам, отмеченным тэгом: {old_tag}. '
                       f'Причина: {str(e)}.')

    except Exception as e:
        logger.warning(f'Не удалось обновить тэги постам, отмеченным тэгом: {old_tag}. '
                       f'Причина: {str(e)}.')

