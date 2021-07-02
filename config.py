import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


class Config:
    DEBUG = bool(os.environ['DEBUG'])
    TESTING = False
    DB_URL = os.environ['DB_URL']
    GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']


class TestingConfig(Config):
    TESTING = True
