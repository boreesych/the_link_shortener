import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_key')
