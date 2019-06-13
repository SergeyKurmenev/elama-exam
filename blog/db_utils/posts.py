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

    Принимает словарь:
    {
    user_id:   int,
    title:     str,
    body:      str,
    is_draft:  bool,
    tag:       str
    }

    is_draft - опциональный флаг для пометки поста в кач-ве черновика.(default=False)
    tag - опциональная строка для указания категории поста (default=None)

    Перед попыткой создания поста производится проверка корректности полученного
    user_id и проверка количества символов в title и body
    (допустимые значения указаны в классе Config - в config.py)

    В случае ошибки при попытке создания поста
    или провале валидации полей происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:

        # Проверка существования категории с данным тэгом
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
        logger.warning("Не удалось создать пост с предоставленными данными. "
                       f"Причина: {str(e)}")
        raise Exception("Не корректные данные. "
                        "Категория с данным тэгом не найдена.")

    except IntegrityError as e:
        db.session.rollback()
        logger.warning("Не удалось создать пост с предоставленными данными. "
                       f"Причина: {str(e)}")
        raise Exception("Не корректные данные. "
                        "Проверьте наличие всех обязательных полей в запросе.")

    except DataError as e:
        db.session.rollback()
        logger.warning('Не удалось создать новый пост. '
                       f'Причина: {str(e)}')
        if 'InvalidTextRepresentation' in str(e):
            raise Exception('Проверьте корректность поля user_id.')
        elif 'StringDataRightTruncation' in str(e):
            raise Exception('Ошибка при попытке создания поста. '
                            'Проверьте количество символов в заголовке и тексте поста. '
                            'Максимально допустимое значение для заголовка - '
                            f'{Config.POST_TITLE_MAX_LENGTH} символов, '
                            f'для текста - {Config.POST_BODY_MAX_LENGTH} символов.')

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.warning('Не удалось создать новый пост. '
                       f'Причина: {str(e)}')
        raise Exception('БД временно недоступна')


def get_all_posts():
    """Метод получения всех постов из БД.

    Возвращает список всех постов(список объектов Post),
    не отмеченных как "черновик".

    [ {id:       int,
      user_id:   int,
      title:     str,
      body:      str,
      is_draft:  bool,
      tag:       str
      },
      ... ,
      {} ]

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

    В качестве входных параметров принимает список id:int постов,
    которые необходимо удалить.

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

    except SQLAlchemyError as e:
        logger.warning(f'Ошибка при попытке удаления постов: {[*args]}. '
                       f'Причина: {str(e)}.')
        raise Exception('БД временно недоступна')


def change_post_tag(post_id: int, tag: str):
    """Метод добавления/изменения тэга поста

    В качестве входных параметров принимает:
    id поста(для которого производить замену) и новый тэг.

    post_id:  int,
    tag:      str

    tag - в случае None значения - у поста будет удалён тэг
        (выставлено значение null - пост без категории)

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
    """Метод получения всех постов категории.

    В качестве входного параметра принимает тэг категории
    посты которой необходимо найти.

    Возвращает список объектов класса Post, которые
    отмечены данным тэгом.

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

