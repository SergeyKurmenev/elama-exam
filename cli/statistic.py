import click
import requests


@click.group(help='Методы работы со статистикой')
def statistic():
    pass


@click.command(help='Метод получения статистики')
def get_statistic():
    response = requests.get('http://127.0.0.1:5000/api/v1/statistic')
    print(response.json(), f"Status code: {response.status_code}")


statistic.add_command(get_statistic)

if __name__ == '__main__':
    statistic()

