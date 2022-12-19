import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    POSTGRES_URL = os.environ.get('POSTGRES_URL',
                                  'postgresql://postgres:postgres@db:5432/')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'flaskrecipes_development')
    SQLALCHEMY_DATABASE_URI = POSTGRES_URL + POSTGRES_DB
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db', 'migrate')

    CELERY_CONFIG = {
        "broker_url": os.environ.get('REDIS_URL', 'redis://redis:6379/0'),
        "result_backend": os.environ.get('REDIS_URL', 'redis://redis:6379/0'),
    }

    CSRF_ENABLED = True
    SECRET_KEY = os.environ['FLASK_RECIPES_SECRET_KEY']


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    POSTGRES_URL = os.environ.get('POSTGRES_URL',
                                  'postgresql://postgres:postgres@db:5432/')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'flaskrecipes_test')
    SQLALCHEMY_DATABASE_URI = POSTGRES_URL + POSTGRES_DB

    CELERY_CONFIG = {
        "broker_url": os.environ.get('REDIS_URL', 'redis://redis:6379/1'),
        "result_backend": os.environ.get('REDIS_URL', 'redis://redis:6379/1'),
    }


class ProductionConfig(Config):
    DEBUG = False
    POSTGRES_URL = os.environ.get('POSTGRES_URL',
                                  'postgresql://postgres:postgres@db:5432/')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'flaskrecipes_production')
    SQLALCHEMY_DATABASE_URI = POSTGRES_URL + POSTGRES_DB
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db', 'migrate')

    CELERY_CONFIG = {
        "broker_url": os.environ.get('REDIS_URL', 'redis://redis:6379/0'),
        "result_backend": os.environ.get('REDIS_URL', 'redis://redis:6379/0'),
    }

    CSRF_ENABLED = True
    SECRET_KEY = os.environ['FLASK_RECIPES_SECRET_KEY']


config = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig
}

SELECTED_CONFIG = os.environ.get("FLASK_ENV", "development")
