import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES_HOST = 'postgres://postgres@flaskrecipes_db_1:5432/'
POSTGRES_DB = 'flaskrecipes_development'
SQLALCHEMY_DATABASE_URI = POSTGRES_HOST + POSTGRES_DB
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = os.getenv('FLASK_RECIPES_SECRET_KEY', 'Eez0ohZe-Eizah5ac-oot4AeSh-dooxea7U-od9Ieroi-eeJ0Aice-Yohnie0o-yohQuei8')
