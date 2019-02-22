#!/usr/bin/env bash

set -e

isort -rc actioner/ tests/

black actioner/ tests/
