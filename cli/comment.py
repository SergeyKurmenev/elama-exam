import click
import json
import requests


@click.group(help='Методы работы с комментариями')
def comment():
    pass


@click.command(help='Метод добавления комментария к посту')
@click.option('--post-id', '-i', help='Id поста к которому относится комментарий')
@click.option('--email', '-e', help='Email оставившего комментарий')
@click.option('--name', '-n', help='Имя оставившего комментарий')
@click.option('--text', '-t', help='Текст комментария')
def make_comment(post_id, email, name, text):
    data = {}

    if post_id:
        data['post_id'] = post_id
    if email:
        data['email'] = email
    if name:
        data['name'] = name
    if text:
        data['text'] = text

    response = requests.post('http://127.0.0.1:5000/api/v1/comments', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))
        click.echo(json.dumps(obj=response.json(),
                              indent=2,
                              sort_keys=True))


@click.command(help='Получение всех комментариев поста')
@click.option('--post-id', '-i', help='Id поста комментарии которого необходимо получить')
def get_comments(post_id):
    data = {}

    if post_id:
        data['post_id'] = post_id

    response = requests.get('http://127.0.0.1:5000/api/v1/comments', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))

    click.echo(response.json())


comment.add_command(make_comment)
comment.add_command(get_comments)


if __name__ == '__main__':
    comment()

