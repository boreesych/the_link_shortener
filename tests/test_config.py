import os

from yacut import app


def test_env_vars(client):
    assert 'sqlite:///db.sqlite3' in list(os.environ.values()), (
        'Добавьте переменную окружение для базы данных со значением sqlite:///db.sqlite3'
    )


def test_config():
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite3', (
        'Укажите значение переменной окружения DB'
    )
    assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    assert app.config['SECRET_KEY'] == os.getenv('SECRET_KEY')
