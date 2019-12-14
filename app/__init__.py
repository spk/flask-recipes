from .extensions import db, ma
from celery import Celery
from flask import Flask
from flask import g
from flask_bootstrap import Bootstrap
from .config import config, SELECTED_CONFIG
from .views import recipes

def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.app = app
    return celery

def create_before_request(app):
    def before_request():
        g.db = db
    return before_request

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[SELECTED_CONFIG])
    db.init_app(app)
    app.register_blueprint(recipes)

    ma.init_app(app)
    Bootstrap(app)

    app.before_request(create_before_request(app))
    return app
