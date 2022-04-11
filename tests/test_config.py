import os

from yacut import app


def test_env_vars():
    assert 'DB' in os.environ, 'Добавьте переменную окружение DB'


def test_config():
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite3', (
        'Укажите значение переменной окружения DB'
    )
    assert not app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    assert app.config['SECRET_KEY'] == os.getenv('SECRET_KEY')
