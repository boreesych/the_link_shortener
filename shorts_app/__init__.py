from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

from dotenv import load_dotenv
load_dotenv()


ID_LENGHT = 6

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
Migrate(app, db)

from shorts_app import api_views, views
