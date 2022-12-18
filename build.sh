#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install
poetry update

python3 manage.py collectstatic --no-input
python3 manage.py migrate
