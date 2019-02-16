#!/usr/bin/env bash

set -e

echo "> Running tests..."
nose2 $@ -C --coverage actioner --verbose --coverage-report term --coverage-report html

echo "> Running isort"
isort -rc -c actioner/ tests/

echo "> Running mypy"
mypy actioner/ tests/

echo "> Running flake8"
flake8 actioner tests
