def test_env_vars(user_environment):
    assert 'sqlite:///db.sqlite3' in list(user_environment.values()), (
        'Проверьте наличие переменной окружения с настройками для подключения'
        ' базы данных со значением `sqlite:///db.sqlite3`.'
    )


def test_config(default_app):
    assert default_app.config.get('SECRET_KEY'), (
        'Проверьте, что задали значение для конфигурационного ключа '
        '`SECRET_KEY`.'
    )
