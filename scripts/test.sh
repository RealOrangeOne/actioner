#!/usr/bin/env bash

set -e

echo "> Running isort"
isort -rc -c actioner/

echo "> Running mypy"
mypy --ignore-missing-imports actioner/

echo "> Running flake8"
flake8 --extend-ignore=E128,E501 actioner
