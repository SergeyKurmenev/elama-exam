from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm.exc import NoResultFound

from loguru import logger

from blog import db

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

    # Проверка корректности предоставленного user_id
    try:
        user_id = int(user_id)
    except Exception as e:
        logger.warning('Не удалось создать пост. Не корректный user_id: {}'.format(user_id))
        raise Exception('Не удалось создать новый пост с предоставленными данными. '
                        'Проверьте корректность поля user_id.')

    # Валидация поля title
    if len(title) >= Config.POST_TITLE_MAX_LENGTH:
        warning_massage = 'Не удалось создать новый пост. ' \
                          'Причина: превышено количество символов в заголовке. ' \
                          'Максимально допустимое количество символов: {}'.format(Config.POST_TITLE_MAX_LENGTH)
        logger.warning(warning_massage)
        raise Exception(warning_massage)

    # Валидация поля body
    if len(body) >= Config.POST_BODY_MAX_LENGTH:
        warning_massage = 'Не удалось создать новый пост. ' \
                          'Причина: превышено количество символов в тексте сообщения. ' \
                          'Максимально допустимое количество символов: {}'.format(Config.POST_BODY_MAX_LENGTH)
        logger.warning(warning_massage)
        raise Exception(warning_massage)

    # Добавление поста, созданного из предоставленных данных, в БД
    try:
        post_for_add = Post(user_id=user_id,
                            title=title,
                            body=body,
                            is_draft=is_draft,
                            tag=tag)

        db.session.add(post_for_add)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.warning('Не удалось создать новый пост. '
                       'Причина: {}'.format(str(e)))
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
                       'Причина: {}.'.format(str(e)))
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
                db.session.delete(post)
            except NoResultFound as e:
                logger.warning("Пост c id: {} не удалён. "
                               "Причина: {}".format(post_id, e))

        db.session.commit()

    except SQLAlchemyError as e:
        logger.warning('Ошибка при попытке удаления постов: {}. '
                       'Причина: {}.'.format([*args], str(e)))
        raise Exception('БД временно недоступна')


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

    statistic = {'post_count': None,
                 'draft_count': None}

    try:
        post_count = Post.query.filter(Post.is_draft == False).count()
        statistic['post_count'] = post_count

        draft_count = Post.query.filter(Post.is_draft == True).count()
        statistic['draft_count'] = draft_count

    except SQLAlchemyError as e:
        logger.warning("Не удалось получить статистику. Причина: {}".format(e))
        raise Exception('БД временно недоступна')

    return statistic


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
        try:
            if tag:
                Category.query.filter(Category.tag == tag).one()
        except NoResultFound as e:
            logger.warning('Тэг для поста с id: {} не изменён. Причина: тэг {} не найден в БД. '
                           'Error massage: "{}"'.format(post_id, tag, str(e)))
            raise Exception('Данный тэг не найден в БД. '
                            'Проверьте правильность написания тэга или создайте новую категорию')

        # Проверка на существование поста с данным id и замена его тэга на новый
        try:
            post_for_change_tag = Post.query.filter(Post.id == post_id).one()
            post_for_change_tag.tag = tag
        except NoResultFound as e:
            logger.warning('Тэг для поста с id: {} не изменён. Причина: пост не найден. '
                           'Error massage: "{}"'.format(post_id, str(e)))
            raise Exception('Пост с данным id не найден в БД')

        db.session.commit()

    except SQLAlchemyError as e:
        logger.warning('Тэг для поста с id: {} не изменён. Причина: {}'.format(post_id, e))
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
        logger.warning('Не удалось получить посты, отмеченные тэгом: {}. '
                       'Причина: {}.'.format(tag, str(e)))
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
        logger.warning('Не удалось обновить тэги постам, отмеченным тэгом: {}. '
                       'Причина: {}.'.format(old_tag, str(e)))

    except Exception as e:
        logger.warning('Не удалось обновить тэги постам, отмеченным тэгом: {}. '
                       'Причина: {}.'.format(old_tag, str(e)))

