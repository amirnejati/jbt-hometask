import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))


class Config:
    DEBUG = bool(os.environ['DEBUG'])
    TESTING = False
    SQLALCHEMY_DB_URL = os.environ['SQLALCHEMY_DB_URL']
    REDIS_URL = os.environ['REDIS_URL']
    GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']


class TestingConfig(Config):
    TESTING = True
