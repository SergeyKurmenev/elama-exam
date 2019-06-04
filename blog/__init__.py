from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

api = Api(app)


from blog import models
from blog import server_api
from blog.resources.posts import Posts
from blog.resources.statistic import Statistic
from blog.resources.comments import Comments
