import click
import requests


@click.group(help='Методы работы с постами')
def post():
    pass


@click.command(help='Метод создания нового поста')
@click.option('--user-id', '-i', help='Id пользователя, который добавляет пост')
@click.option('--title', '-t', help='Заголовок поста')
@click.option('--body', '-b', help='Текст поста')
@click.option('--is-draft', '-D', help='Пометка "черновик"(опциональный параметр, '
                                       'что бы сохранить черновик - необходимо установить "True")')
@click.option('--tag', '-T', help='Тэг категории к которому причислить пост(опционально)')
def make_post(user_id, title, body, is_draft, tag):
    data = {}

    if user_id:
        data["user_id"] = user_id
    if title:
        data["title"] = title
    if body:
        data["body"] = body
    if is_draft:
        data["is_draft"] = is_draft
    if tag:
        data["tag"] = tag

    response = requests.post('http://127.0.0.1:5000/api/v1/posts', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))
        click.echo(response.json())


@click.command(help='Метод добавления/изменения тэга поста')
@click.option('--post-id', '-i', help='Id поста для которого будет производиться замена тэга')
@click.option('--tag', '-t', help='Новый тэг, который необходимо присвоить посту')
def change_tag(post_id, tag):
    data = {}

    if post_id:
        data['post_id'] = post_id
    if tag:
        data['tag'] = tag

    response = requests.put('http://127.0.0.1:5000/api/v1/posts', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))
        click.echo(response.json())


@click.command(help='Метод удаления постов')
@click.option('--posts-id', '-i', help='Id постов, которые необходимо удалить. '
                                       'При удалении нескольких постов - id перечисляются через ","')
def delete_posts(posts_id):
    data = {}

    if posts_id:
        data['posts_id'] = posts_id

    response = requests.delete('http://127.0.0.1:5000/api/v1/posts', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))
        click.echo(response.json())


post.add_command(make_post)
post.add_command(change_tag)
post.add_command(delete_posts)


if __name__ == '__main__':
    post()

