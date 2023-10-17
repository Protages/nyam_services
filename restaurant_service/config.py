import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_URL = os.environ.get('SQLITE_URL')
ASYNC_SQLITE_URL = os.environ.get('ASYNC_SQLITE_URL')
