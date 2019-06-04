from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

from blog import db

from blog.models import Post


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

    """

    post_for_add = Post(user_id=user_id,
                        title=title,
                        body=body,
                        is_draft=is_draft,
                        tag=tag)

    db.session.add(post_for_add)
    try:
        db.session.commit()
    except OperationalError as e:
        db.session.rollback()
        raise Exception(str(e))


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

    """

    posts = Post.query.filter(Post.is_draft == False).all()
    return posts


def delete_posts(*args: int):
    """Метод удаления постов из БД.

    В качестве входных параметров принимает список id:int постов,
    которые необходимо удалить.

    """

    for post_id in args:
        try:
            post = Post.query.filter(Post.id == post_id).one()
            db.session.delete(post)
            db.session.commit()
        except SQLAlchemyError:
            # TODO: Добавить обработку исключений при попытке удалении поста
            pass


def get_statistic():
    """Метод получения статистики постов из БД.

    Возвращает словарь из двух элементов: количество постов и количество черновиков.

    {
    post_count:  int,
    draft_count: int
    }

    """

    statistic = {'post_count': 0,
                 'draft_count': 0}

    posts = Post.query.filter(Post.is_draft == False).all()
    post_count = len(posts)

    drafts = Post.query.filter(Post.is_draft == True).all()
    draft_count = len(drafts)

    statistic['post_count'] = post_count
    statistic['draft_count'] = draft_count

    # TODO: Добавить обработку исключений при попытках обращений к БД
    return statistic


def change_post_tag(post_id: int, tag: str):
    """Метод добавления/изменения тэга поста

    В качестве входных параметров принимает список:
    id поста(для которого производить замену) и новый тэг.

    post_id:  int,
    tag:      str

    """

    # TODO: Добавить обработку исключений при обращении к БД
    post_for_change_tag = Post.query.filter(Post.id == post_id).first()
    post_for_change_tag.tag = tag

    db.session.commit()


def get_posts_with_tag(tag: str):
    """Метод получения всех постов категории.

    В качестве входного параметра принимает тэг категории
    посты которой необходимо найти.

    Возвращает список объектов класса Post, которые
    отмечены данным тэгом.
    """

    posts = Post.query.filter(Post.tag == tag).all()
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

    """

    posts = get_posts_with_tag(old_tag)

    for post in posts:
        post.tag = new_tag

    db.session.commit()

