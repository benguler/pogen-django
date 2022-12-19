#!/usr/bin/env bash
# exit on error
set -o errexit

poetry update
poetry lock
poetry install

python3 manage.py collectstatic --no-input
python3 manage.py migrate
