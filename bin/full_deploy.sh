#!/bin/bash

# Создание БД
source ./bin/create_db.sh

# Создание и активация виртуального окружения
source ./bin/deploy_virtualenv.sh

# Подготовка БД
source ./bin/prepare_db.sh

# Заполнение БД тестовыми данными
python fill_db_with_demo_data.py

