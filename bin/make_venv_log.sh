#!/bin/bash

log_file="./logs/virtualenv/venv.`date '+%Y-%m-%d_%H-%M'`.log"

python --version >> ${log_file}

echo '====================' >> ${log_file}

echo 'requirements.txt:' >> ${log_file}
echo >> ${log_file}
cat requirements.txt >> ${log_file}

echo '====================' >> ${log_file}

echo 'pip freeze:' >> ${log_file}
echo >> ${log_file}
pip freeze >> ${log_file}

echo '====================' >> ${log_file}

