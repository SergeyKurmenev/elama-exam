from blog import db

from config import Config


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(Config.POST_TITLE_MAX_LENGTH), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_draft = db.Column(db.Boolean, nullable=False)
    tag = db.Column(db.String(Config.TAG_MAX_LENGTH), nullable=True)

    def __init__(self,
                 user_id: int,
                 title: str,
                 body: str,
                 is_draft: bool = False,
                 tag: str = None):

        self.user_id = user_id
        self.title = title
        self.body = body
        self.is_draft = is_draft
        self.tag = tag


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.string(Config.COMMENT_TITLE_MAX_LENGTH), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(self,
                 post_id: int,
                 email: str,
                 name: str,
                 body: str):

        self.post_id = post_id
        self.email = email
        self.name = name
        self.body = body


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.string(Config.CATEGORY_NAME_MAX_LENGTH), nullable=False)
    tag = db.Column(db.String(Config.TAG_MAX_LENGTH), nullable=True)

