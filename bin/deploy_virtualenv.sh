#!/bin/bash

# Создаётся виртуальное окружение, производится установка зависимостей,
# полная информация о собранном виртуальном окружении
# записывается в лог-файл ./logs/virtualenv/venv.<дата_время>.log

virtualenv -p python3 ./venv
source ./venv/bin/activate
pip install -r requirements.txt

#Эта часть отвечает за создание лога
source ./bin/make_venv_log.sh

