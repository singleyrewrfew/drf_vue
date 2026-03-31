#!/bin/bash

echo "Running tests..."

echo "Running Django tests..."
python manage.py test

echo "Running flake8 code quality check..."
flake8 . --max-line-length=120 --exclude=migrations,settings.py,venv,env

echo "All tests completed!"
