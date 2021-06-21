import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    # CSRF_ENABLED = True
    # SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DB_URI = os.environ['DB_URL']

    # x = os.getenv()


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
