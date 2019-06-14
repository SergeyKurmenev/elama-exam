import click
import json
import requests


@click.group(help='Методы работы с категориями')
def category():
    pass


@click.command(help='Метод добавления новой категории')
@click.option('--name', '-n', help='Название категории')
@click.option('--tag', '-t', help='Тэг категории')
def make_category(name, tag):
    data = {"name": name,
            "tag": tag}

    response = requests.post('http://127.0.0.1:5000/api/v1/categories', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))
        click.echo(json.dumps(obj=response.json(),
                              indent=2,
                              sort_keys=True,
                              ensure_ascii=False))


@click.command(help='Метод получения всех категорий')
def get_categories():
    response = requests.get('http://127.0.0.1:5000/api/v1/categories')

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))

    click.echo(json.dumps(obj=response.json(),
                          indent=2,
                          sort_keys=True,
                          ensure_ascii=False))


@click.command(help='Метод редактирования категорий')
@click.option('--category-id', '-i', help='Id категории, которую необходимо отредактировать')
@click.option('--name', '-n', help='Новое название категории '
                                   '(опционально, при отсутствии сохраняется старое название)')
@click.option('--tag', '-t', help='Новый тэг категории '
                                  '(опционально, при отсутствии сохраняется старый тэг)')
def change_category(category_id, name, tag):
    data = {}

    if category_id:
        data['category_id'] = category_id
    if name:
        data['name'] = name
    if tag:
        data['tag'] = tag

    response = requests.put('http://127.0.0.1:5000/api/v1/categories', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))
        click.echo(json.dumps(obj=response.json(),
                              indent=2,
                              sort_keys=True,
                              ensure_ascii=False))


@click.command(help='Метод удаления категории')
@click.option('--category-id', '-i', help='Id категории, которую необходимо удалить')
def delete_category(category_id):
    data = {}

    if category_id:
        data['category_id'] = category_id

    response = requests.delete('http://127.0.0.1:5000/api/v1/categories', data=data)

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))
        click.echo(json.dumps(obj=response.json(),
                              indent=2,
                              sort_keys=True,
                              ensure_ascii=False))


category.add_command(change_category)
category.add_command(delete_category)
category.add_command(get_categories)
category.add_command(make_category)


if __name__ == '__main__':
    category()

