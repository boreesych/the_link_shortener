from sqlalchemy import inspect

# from yacut import db
from yacut.models import URL_map


def test_fields(_app):
    # assert db.engine.table_names() == ['URL_map'], (
    #     'Не обнаружена таблица URL_map'
    # )
    # a = inspect(db.engine)
    # assert a.has_table('URL_map'), 'Не обнаружена таблица URL_map'

    inspector = inspect(URL_map)
    fields = [column.name for column in inspector.columns]
    print(fields)
    assert all(field in fields for field in ['id', 'original', 'short', 'timestamp']), (
        'В модели не найдены все необходимые поля. '
        'Проверьте модель: в ней должны быть поля id, original, short и timestamp.'
    )