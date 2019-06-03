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

