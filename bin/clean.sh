#!/bin/bash

cd ./db
docker-compose down
cd ..

deactivate
rm -r venv/
rm -r migrations/

