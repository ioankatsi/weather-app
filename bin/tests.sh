#!/bin/bash

# Set the PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Ensure we have everything installed
pip3 install --upgrade pip && pip3 install -r requirements.txt

# Run Alembic migrations
cd app && alembic upgrade head

cd ..

# Run pytest with coverage
pytest --cov=app/tests/basic_unit_tests.py --cov-report=term-missing:skip-covered --cov-report=html

# # Generate a detailed coverage report
coverage report -m