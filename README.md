# Backend часть сервера для блога

---

### Скрипт для создания виртуального окружения

Для создания виртуального окружения 
необходимо из корневой папки проекта выполнить:

```bash
source bin/deploy_virtualenv.sh
```

В результате будет создано виртуальное окружение и 
установлены зависимости из файла `requirements.txt`.
Полная информация о собраном виртуальном окружении сохраняется 
в log-файл: 

`logs/virtualenv/venv.<дата_время>.log`

### Создание БД и заполнение тестовыми данными

Для создания БД из корневой папки проекта необходимо выполнить
следующие команды:

Активировать виртуальное окружение, если не активировано:
```bash
source venv/bin/activate
```
Произвести инициализацию БД:
```bash
python manage.py db init
```
Создать сценарий миграции:
```bash
python manage.py db migrate -m '<Комментарий к миграции>'
```
Создать БД (в данном случае используется SQLite.
БД создаётся в корневой папке проекта `blog.db`):
```bash
python manage.py db upgrade
```

Далее необходимо заполнить БД тестовыми данными.
Для этого необходимо выполнить из корневой папки проекта:
```bash
python fill_db_with_demo_data.py
```
С помощью данного скрипта в БД добавляется 100 постов и
500 комментариев к ним.
Скрипт выполняется довольно медленно - позже будет заменён.
(Скрипт выводит результаты работы в консоль - для отображения того,
что работает)
