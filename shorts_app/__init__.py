from flask import Flask
from settings import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

ID_LENGHT = 6

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from shorts_app import views
from shorts_app import api_views
