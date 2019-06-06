from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm.exc import NoResultFound

from loguru import logger

from blog import db

from blog.models import Category

from blog.db_utils.posts import refresh_tag


def add_category(name: str, tag: str):
    """Метод добавления новой категории в БД.

    В качестве входных параметров принимает список: имя категории и тэг категории.

    {
    name:  str,
    tag:   str
    }

    При невозможности записи в БД просиходит raise Exception
    с сообщением, соответствующим причине ошибки.

    """

    category_for_add = Category(name=name,
                                tag=tag)

    db.session.add(category_for_add)

    try:
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        logger.warning('Не удалось добавить новую категорию в БД. Причина: {}'.format(e))
        raise Exception('Не корректные данные, возможно такая категория или тэг уже заняты')

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.warning('Не удалось добавить новую категорию в БД. Причина: {}'.format(e))
        raise Exception('БД временно недоступна')


def get_all_categories():
    """Метод получения списка всех категорий из БД.

    Возвращает список всех категорий(список объектов Category).

    [
      {
      id:    int,
      name:  str,
      tag:   str
      },
      ... ,
      {}
    ]

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением об ошибке.

    """

    try:
        categories = Category.query.all()
    except SQLAlchemyError as e:
        logger.warning('Не удалось получить категории из БД. Причина: {}'.format(e))
        raise Exception('БД временно недоступна')

    return categories


def change_category(category_id: int, name: str = None, tag: str = None):
    """Метод редактирования категории.

    В качестве входных параметров принимает список:
    id категории(которую редактировать), name - новое имя, tag - новый тэг.

    category_id:  int,
    name:         str,
    tag:          str

    name - опционально(default=None - имя сохраняется старое)
    tag - опционально(default=None - тэг сохраняется старый)

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:
        category_for_change = Category.query.filter(Category.id == category_id).one()

        old_tag = None

        if name:
            category_for_change.name = name
        if tag:
            old_tag = category_for_change.tag
            category_for_change.tag = tag

        db.session.commit()

    except NoResultFound as e:
        logger.warning('Редактирование категории с id: {} не удалось. '
                       'Причина: категория не найдена. Error massage: "{}"'.format(category_id, str(e)))
        raise Exception('Категория с данным id не найдена в БД')

    except IntegrityError as e:
        logger.warning('Редактирование категории с id: {} не удалось. '
                       'Причина: не корректные данные. Error massage: "{}"'.format(category_id, str(e)))
        raise Exception('Ошибка при попытке редактирования. '
                        'Возможно данное имя или тэг уже заняты.')

    except SQLAlchemyError as e:
        logger.warning('Редактирование категории с id: {} не удалось. '
                       'Причина: "{}"'.format(category_id, str(e)))
        raise Exception('БД временно недоступна')

    if old_tag:
        # обновление тэга во всех постах, которые на него ссылались
        refresh_tag(old_tag=old_tag,
                    new_tag=tag)

