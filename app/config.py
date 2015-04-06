import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    POSTGRES_HOST = 'postgres://postgres@db:5432/'
    POSTGRES_DB = 'flaskrecipes_development'
    SQLALCHEMY_DATABASE_URI = POSTGRES_HOST + POSTGRES_DB
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db', 'migrate')

    CELERY_BROKER_URL='redis://redis:6379/0'
    CELERY_RESULT_BACKEND='redis://redis:6379/0'

    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('FLASK_RECIPES_SECRET_KEY', 'Eez0ohZe-Eizah5ac-oot4AeSh-dooxea7U-od9Ieroi-eeJ0Aice-Yohnie0o-yohQuei8')

class TestConfig(Config):
    DEBUG = False
    TESTING = True
    POSTGRES_HOST = 'postgres://postgres@db:5432/'
    POSTGRES_DB = 'flaskrecipes_test'
    SQLALCHEMY_DATABASE_URI = POSTGRES_HOST + POSTGRES_DB

config = {"development": DevelopmentConfig, "test": TestConfig}

SELECTED_CONFIG = os.getenv("FLASK_ENV", "development")
