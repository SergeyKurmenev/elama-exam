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

    def to_dict(self):
        post = {'id': self.id,
                'user_id': self.user_id,
                'title': self.title,
                'body': self.body,
                'tag': self.tag}

        return post


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(Config.COMMENT_TITLE_MAX_LENGTH), nullable=False)
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

    def to_dict(self):
        comment = {'id': self.id,
                   'post_id': self.post_id,
                   'email': self.email,
                   'name': self.name,
                   'body': self.body}

        return comment


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(Config.CATEGORY_NAME_MAX_LENGTH), nullable=False)
    tag = db.Column(db.String(Config.TAG_MAX_LENGTH), nullable=True)

    def __init__(self,
                 name: str,
                 tag: str):

        self.name = name
        self.tag = tag

