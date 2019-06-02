from urllib.request import urlopen
import json

from blog.db_utils.posts import add_post

from blog.db_utils.comments import add_comment

posts_url = "https://jsonplaceholder.typicode.com/posts"
comments_url = "https://jsonplaceholder.typicode.com/comments"

count = 1
posts = json.loads(urlopen(posts_url).read())
for post in posts:
    add_post(user_id=post['userId'],
             title=post['title'],
             body=post['body'])
    print('post {} done'.format(count))
    count += 1


count = 1
comments = json.loads(urlopen(comments_url).read())
for comment in comments:
    add_comment(post_id=comment['postId'],
                email=comment['email'],
                name=comment['name'],
                body=comment['body'])
    print('comment {} done'.format(count))
    count += 1

