from sqlalchemy.exc import DataError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm.exc import NoResultFound

from loguru import logger

from blog import db

from blog.models import Category

from blog.db_utils.posts import refresh_tag


def add_category(name: str, tag: str):
    """Метод добавления новой категории в БД.

    В качестве входных параметров принимает:

    name:  str  -  Имя категории
    tag:   str  -  Тэг категории

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
        logger.warning(f'Не удалось добавить новую категорию в БД. Причина: {str(e)}')

        if 'NotNullViolation' in str(e):
            raise Exception('Не корректные данные. '
                            'Не все обязательные поля заполнены.')

        raise Exception('Не корректные данные. '
                        'Возможно такая категория или тэг уже заняты')

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.warning(f'Не удалось добавить новую категорию в БД. Причина: {str(e)}')
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
        logger.warning(f'Не удалось получить категории из БД. Причина: {str(e)}')
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

    except DataError as e:
        logger.warning(f'Редактирование категории с id: {category_id} не удалось. '
                       f'Причина: {str(e)}')
        raise Exception('Ошибка при попытке редактирования. '
                        'Не корректный id категории.')

    except NoResultFound as e:
        logger.warning(f'Редактирование категории с id: {category_id} не удалось. '
                       f'Причина: категория не найдена. Error massage: "{str(e)}"')
        raise Exception('Категория с данным id не найдена в БД')

    except IntegrityError as e:
        logger.warning(f'Редактирование категории с id: {category_id} не удалось. '
                       f'Причина: не корректные данные. Error massage: "{str(e)}"')
        raise Exception('Ошибка при попытке редактирования. '
                        'Возможно данное имя или тэг уже заняты.')

    except SQLAlchemyError as e:
        logger.warning(f'Редактирование категории с id: {category_id} не удалось. '
                       f'Причина: "{str(e)}"')
        raise Exception('БД временно недоступна')

    if old_tag:
        # обновление тэга во всех постах, которые на него ссылались
        refresh_tag(old_tag=old_tag,
                    new_tag=tag)


def delete_category(category_id: int):
    """Метод удаления категории.

    В качестве входного параметра принимает id категории,
    которую необходимо удалить.

    category_id: int

    В случае ошибки при обращении к БД происходит
    raise Exception с сообщением, соответствующим причине ошибки.

    """

    try:
        category_for_delete = Category.query.filter(Category.id == category_id).one()
        refresh_tag(category_for_delete.tag, None)

        db.session.delete(category_for_delete)
        db.session.commit()

    except DataError as e:
        logger.warning('Ошибка при попытке удаления категории. '
                       f'Причина: не корректный id - {category_id}. '
                       f'Error message: {str(e)}')
        raise Exception('Проверьте корректость id удаляемой категории.')

    except NoResultFound as e:
        logger.warning(f'Удаление категории с id: {category_id} не удалось. '
                       f'Причина: категория не найдена. Error message: "{str(e)}"')
        raise Exception('Проверьте корректость id удаляемой категории.')

    except SQLAlchemyError as e:
        logger.warning(f'Удаление категории с id: {category_id} не удалось. '
                       f'Причина: "{str(e)}"')
        raise Exception('БД временно недоступна')

