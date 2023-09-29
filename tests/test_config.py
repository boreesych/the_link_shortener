import os


def test_env_vars(user_environment):
    assert 'sqlite:///db.sqlite3' in list(user_environment.values()), (
        'Проверьте наличие переменной окружения с настройками для подключения'
        ' базы данных со значением `sqlite:///db.sqlite3`.'
    )


def test_config(default_app, tmp_db_uri, user_environment):
    assert default_app.config['SQLALCHEMY_DATABASE_URI'] == tmp_db_uri, (
        'Проверьте, что конфигурационному ключу `SQLALCHEMY_DATABASE_URI` '
        'присвоено значение с настройками для подключения базы данных с '
        'использованием переменной окружения `DATABASE_URI`.'
    )
    SECRET_KEY = os.getenv('SECRET_KEY')
    assert SECRET_KEY, (
        'Проверьте, что конфигурационному ключу `SECRET_KEY` '
        'присвоено значение.'
    )
    assert default_app.config['SECRET_KEY'] == SECRET_KEY, (
        'Проверьте, что значение для конфигурационного ключа `SECRET_KEY` '
        'задается через переменную окружения `SECRET_KEY`.'
    )
