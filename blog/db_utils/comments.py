from sqlalchemy.exc import OperationalError

from blog import db

from blog.models import Comment


def add_comment(post_id: int, email: str, name: str, body: str):
    """Метод добавления комментария.

    Принимает словарь:
    {
    post_id:   int,
    email:     str,
    name:      str,
    body:      bool,
    }

    """

    comment_for_add = Comment(post_id=post_id,
                              email=email,
                              name=name,
                              body=body)

    db.session.add(comment_for_add)
    try:
        db.session.commit()
    except OperationalError as e:
        db.session.rollback()
        raise Exception(str(e))

