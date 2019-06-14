# Backend часть сервера для блога

Для работы необходимо наличие установленного `docker`, `docker-compose` 
и `virtualenv`.

---

### Документация `api`:

Для `api` сгенерирована документация(с использованием `swagger`).

Она доступна после запуска приложения по ссылкам:

- [В виде HTML](http://localhost:5000/api/spec.html#!/spec)
  - в html форме реализована возможность запросов к `api`.

- [В виде JSON](http://localhost:5000/api/spec.json)

---
### Тестовые данные, используемые, для заполнения бд:

- [Посты](https://jsonplaceholder.typicode.com/posts)

- [Комментарии](https://jsonplaceholder.typicode.com/comments)
---

### Скрипт полной сборки и запуска:

Для полной сборки и запуска необходимо из корневой папки проекта выполнить команду:

```bash
source ./bin/deploy_and_start.sh
```

В результате будет выполнено:
* запущенна БД `PostgeSQL` с помощью `docker-compose`
* создано и активировано виртуальное окружение
* установлены зависимости из `requiremens.txt`
* созданы необходимые таблицы в БД
* БД заполнена тестовыми данными
* запущен проект

---

### Запуск и остановка:

Запуск осуществляется выполнением из корневой папки проекта команды:

```bash
python runserver.py
```

Для остановки использовать `CTRL+C`.

---

### CLI:

Взаимодействие с `api` возможно с помощью `CLI`.
Запуск осуществляется с помошью комманды из корневой папки проекта:
```bash
python cli/<Название тестируемой части>.py
```
Тестируемые части:
* category
  
  команды:
  * change-category
  * delete-category
  * get-categories
  * make-category
  
* comment
  
  команды:
  * get-comments
  * make-comment

* post  

  команды:
  * change-tag
  * delete-posts
  * get-all-posts
  * make-post

* statistic
  
  команды:
  * get-statistic
  
Что бы посмотреть опции комманды необходимо 
выполнить комманду с опцией `--help`. 

Пример:
```bash
python cli/post.py delete-posts --help
```
---

### Скрипт для полной сборки приложения

Скрипт объединяет в себе создание БД, скрипт создания виртуального окружения, 
подготовку БД и скрипт заполнения БД тестовыми данными.

Для полного развёртывания необходимо из корневой папки проекта выполнить команду:

```bash
source ./bin/full_deploy.sh
```

---

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

---

### Создание БД:

Для создания БД из корневой папки проекта необходимо выполнить команду:

```bash
source ./bin/create_db.sh
```
---

### Подготовка БД: 

Для подготовки БД из корневой папки проекта необходимо выполнить
следующие команды:

Активировать виртуальное окружение, если не активировано:

```bash
source venv/bin/activate
```

#### Далее выполнить скрипт:

```bash
source ./bin/prepare_db.sh
```

#### или последовательность команд:



Произвести инициализацию:

```bash
python manage.py db init
```

Создать сценарий миграции:

```bash
python manage.py db migrate -m '<Комментарий к миграции>'
```

Провести создание таблиц в БД:

```bash
python manage.py db upgrade
```

---

### Скрипт заполнения БД тестовыми данными

Для заполнения БД тестовыми данными необходимо 
выполнить из корневой папки проекта:

```bash
python fill_db_with_demo_data.py
```

С помощью данного скрипта в БД добавляется:
* 5 категорий
* 100 постов(с маркировкой созданными категориями)
* 500 комментариев к постам
* 100 черновиков. 

