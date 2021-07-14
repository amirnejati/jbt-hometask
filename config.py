import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))


class Config:
    DEBUG = bool(os.environ['DEBUG'])
    TESTING = False
    SQLALCHEMY_DB_URL = os.environ['SQLALCHEMY_DB_URL']
    REDIS_URL = os.environ['REDIS_URL']
    ALLOWED_REQUESTS_PER_MINUTE = int(os.getenv('ALLOWED_REQUESTS_PER_MINUTE', 60))
    THROTTLING_DENY_SECONDS = int(os.getenv('THROTTLING_DENY_SECONDS', 60))
    GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']


class TestingConfig(Config):
    TESTING = True
