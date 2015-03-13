from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.marshmallow import Marshmallow
from flask_bootstrap import Bootstrap

app = Flask(__name__)
ma = Marshmallow(app)
app.config.from_object('config')
db = SQLAlchemy(app)
Bootstrap(app)

from app import views, models
