#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (includes CSS updates)
python manage.py collectstatic --no-input --clear

# Run database migrations
python manage.py migrate
