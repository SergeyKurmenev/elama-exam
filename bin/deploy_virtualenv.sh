#!/bin/bash

# Создаётся виртуальное окружение, производится установка зависимостей,
# полная информация о собранном виртуальном окружении
# записывается в лог-файл ./logs/virtualenv/venv.<дата_время>.log

virtualenv -p python3 ./venv
source ./venv/bin/activate
pip install -r requirements.txt
log_file="./logs/virtualenv/venv.`date '+%Y-%m-%d_%H-%M'`.log"

python --version >> ${log_file}
echo >> ${log_file}
pip freeze >> ${log_file}
