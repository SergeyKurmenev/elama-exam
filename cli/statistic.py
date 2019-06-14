import click
import json
import requests


@click.group(help='Методы работы со статистикой')
def statistic():
    pass


@click.command(help='Метод получения статистики')
def get_statistic():
    response = requests.get('http://127.0.0.1:5000/api/v1/statistic')

    if response.ok:
        click.echo(click.style(f"Status code: {response.status_code}", fg='green'))
    else:
        click.echo(click.style(f"Status code: {response.status_code}", fg='red'))

    click.echo(json.dumps(obj=response.json(),
                          indent=2,
                          sort_keys=True,
                          ensure_ascii=False))


statistic.add_command(get_statistic)

if __name__ == '__main__':
    statistic()

