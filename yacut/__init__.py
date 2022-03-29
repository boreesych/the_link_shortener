from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config


ID_LENGHT = 6

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
Migrate(app, db)

from yacut import api_views, views
