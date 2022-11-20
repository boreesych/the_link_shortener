from datetime import datetime

from . import db


class UrlMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(1024), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    # Тут можно рассказать про различие между 
    # default=datetime.utcnow() и default=datetime.utcnow
    # если подставить вызов функции datetime.utcnow(), 
    # то будет значение, вычисленное при старте приложения, так не надо делать
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
