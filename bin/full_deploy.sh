#!/bin/bash

# Создание и активация виртуального окружения
source ./bin/deploy_virtualenv.sh

# Создание БД
source ./bin/create_db.sh

# Заполнение БД тестовыми данными
python fill_db_with_demo_data.py

