import click
import requests


@click.command()
@click.option('--name', '-n', help='Название категории')
@click.option('--tag', '-t', help='Тэг категории')
def make_category(name, tag):
    data = {"name": name,
            "tag": tag}

    response = requests.post('http://127.0.0.1:5000/api/v1/categories', data=data)
    print(response.status_code)


if __name__ == '__main__':
    make_category()

