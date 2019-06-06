# Backend часть сервера для блога

---

### Запуск 

Запуск осуществляется выполнением из корневой папки проекта команды:

```bash
python runserver.py
```

### Скрипт для полного развёртывания приложения

Скрипт объединает в себе скрипт создания виртуального окружения, создание БД
и скрипт заполнения БД тестовыми данными.

Для полного развёртывания необходимо из корневой папки проекта выполнить команду:

```bash
source ./bin/full_deploy.sh
```


### Скрипт для создания виртуального окружения

Для создания виртуального окружения 
необходимо из корневой папки проекта выполнить:

```bash
source bin/deploy_virtualenv.sh
```

В результате будет создано и активировано виртуальное окружение и 
установлены зависимости из файла `requirements.txt`.
Полная информация о собраном виртуальном окружении сохраняется 
в log-файл: 

`logs/virtualenv/venv.<дата_время>.log`

### Создание БД 

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
БД создаётся в корневой папке проекта):

```bash
python manage.py db upgrade
```


### Скрипт заполнения БД тестовыми данными

Далее необходимо заполнить БД тестовыми данными.
Для заполнения БД тестовыми данными этого необходимо 
выполнить из корневой папки проекта:

```bash
python fill_db_with_demo_data.py
```

С помощью данного скрипта в БД добавляется 100 постов и
500 комментариев к ним.

---
Тестовые данные, используемые, для заполнения бд:

- [Посты](https://jsonplaceholder.typicode.com/posts)

- [Комментарии](https://jsonplaceholder.typicode.com/comments)
---

