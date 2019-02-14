#!/usr/bin/env bash

set -e

echo "> Running isort"
isort -rc -c actioner/

echo "> Running mypy"
mypy actioner/

echo "> Running flake8"
flake8 actioner
