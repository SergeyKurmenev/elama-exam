import click
import requests


@click.command()
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
    if response.status_code == 201:
        print(response.status_code)
    else:
        print(response.json(), f"Status code: {response.status_code}")


if __name__ == '__main__':
    make_post()

