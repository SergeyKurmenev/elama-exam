#!/bin/bash

# Создание БД
cd ./db
docker-compose up -d
cd ..

# Создание и активация виртуального окружения
source ./bin/deploy_virtualenv.sh

# Подготовка БД
source ./bin/prepare_db.sh

# Заполнение БД тестовыми данными
python fill_db_with_demo_data.py

