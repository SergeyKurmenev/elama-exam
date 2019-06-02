from sqlalchemy.exc import OperationalError

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

