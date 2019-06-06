#!/bin/bash

# Создание и активация виртуального окружения
source ./bin/deploy_virtualenv.sh

# Создание БД
python manage.py db init
migrate_massage=`date '+%Y-%m-%d_%H-%M'`
python manage.py db migrate -m "${migrate_massage}"
python manage.py db upgrade

# Заполнение БД тестовыми данными
python fill_db_with_demo_data.py

