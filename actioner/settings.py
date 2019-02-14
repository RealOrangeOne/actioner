import os
from logging import _nameToLevel

from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

LOGGING_LEVEL = _nameToLevel[os.environ.get('LOGGING_LEVEL', 'INFO')]
