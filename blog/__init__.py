from flask import Flask

from flask_restful import Api

from flask_restful_swagger import swagger

from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

api = swagger.docs(Api(app), apiVersion='0.1')


from blog import models

from blog.resources.categories import Categories
from blog.resources.comments import Comments
from blog.resources.posts import Posts
from blog.resources.statistic import Statistic

api.add_resource(Categories, '/api/v1/categories')
api.add_resource(Comments, '/api/v1/comments')
api.add_resource(Posts, '/api/v1/posts')
api.add_resource(Statistic, '/api/v1/statistic')

