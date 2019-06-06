#!/bin/bash

python manage.py db init
migrate_massage=`date '+%Y-%m-%d_%H-%M'`
python manage.py db migrate -m "${migrate_massage}"
python manage.py db upgrade

