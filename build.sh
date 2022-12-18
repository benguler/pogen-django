#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install
poetry lock --no-update

python manage.py collectstatic --no-input
python manage.py migrate
