import os
from logging import _nameToLevel

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

TODOIST_TOKEN = os.environ['TODOIST_TOKEN']

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

LOGGING_LEVEL = _nameToLevel[os.environ.get('LOGGING_LEVEL', 'INFO')]

BASIC_AUTH = os.environ['BASIC_AUTH'].split(":")
