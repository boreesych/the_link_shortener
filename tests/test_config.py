import os


def test_env_vars():
    assert 'sqlite:///db.sqlite3' in list(os.environ.values()), (
        'Добавьте переменную окружение для базы данных со значением sqlite:///db.sqlite3'
    )


def test_config(default_app):
    assert default_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite3', (
        'Укажите значение переменной окружения DB'
    )
    assert not default_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    assert default_app.config['SECRET_KEY'] == os.getenv('SECRET_KEY')
