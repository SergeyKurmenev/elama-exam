from blog import db

from blog.models import Category


def add_category(name: str, tag: str):
    """Метод добавления новой категории в БД.

    В качестве входных параметров принимает список: имя категории и тэг категории.

    {
    name:  str,
    tag:   str
    }

    """

    category_for_add = Category(name=name,
                                tag=tag)

    # TODO: Добавить обработку исключений при попытке добавления в бд
    db.session.add(category_for_add)
    db.session.commit()


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

    """

    # TODO: Добавить обработку исключений при попытке запроса в БД
    categories = Category.query.all()

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

    """

    # TODO: Добавить обработку исключений при обращении к БД
    category_for_change = Category.query.filter(Category.id == category_id).first()

    if name:
        category_for_change.name = name
    if tag:
        category_for_change.tag = tag
        # TODO: добавить вызов метода замены тэгов на актуальные для
        #       ссылавшихся на изменённый тэг постов

    db.session.commit()

