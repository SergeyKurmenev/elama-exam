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


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.string(Config.COMMENT_TITLE_MAX_LENGTH), nullable=False)
    body = db.Column(db.Text, nullable=False)

