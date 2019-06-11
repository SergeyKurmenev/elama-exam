import json

from urllib.request import urlopen

from sqlalchemy.exc import SQLAlchemyError

from blog import db

from blog.models import Category
from blog.models import Post
from blog.models import Comment

categories_count = 5

for number in range(categories_count):
    category_for_add = Category(f'Category number {number + 1}', f'#tag{number + 1}')
    db.session.add(category_for_add)

posts_url = "https://jsonplaceholder.typicode.com/posts"
comments_url = "https://jsonplaceholder.typicode.com/comments"

posts = json.loads(urlopen(posts_url).read())
comments = json.loads(urlopen(comments_url).read())

for post in posts:
    post_for_add = Post(user_id=post['userId'],
                        title=post['title'],
                        body=post['body'])

    db.session.add(post_for_add)

for comment in comments:
    comment_for_add = Comment(post_id=comment['postId'],
                              email=comment['email'],
                              name=comment['name'],
                              body=comment['body'])

    db.session.add(comment_for_add)

try:
    db.session.commit()
except SQLAlchemyError as e:
    print('Не удалось записать занные в БД.'
          f'Причина: {str(e)}')
