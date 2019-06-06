import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POST_TITLE_MAX_LENGTH = 100
    POST_BODY_MAX_LENGTH = 1000

    COMMENT_TITLE_MAX_LENGTH = 100

    CATEGORY_NAME_MAX_LENGTH = 100
    TAG_MAX_LENGTH = 25

