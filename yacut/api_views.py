import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    # Проверить корректность сравнения с None и использование HTTPStatus
    if link is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': link.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    # `request.json` вызывает `.get_json()` с дефолтными параметрами, в том
    # числе `silent=False`. Если тела запроса не окажется в запросе, то
    # автоматически вернется ответ с кодом 400 в виде HTML.
    json_body = request.get_json(silent=True)
    if json_body is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in json_body:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    url = json_body.get('url')
    short_id = json_body.get('custom_id')
    # Возможно стоит вынести эту проверку в отдельный валидатор,
    # так как есть дублирование во view-функции
    if (
        short_id and
        (re.search(r'[^a-zA-Z0-9]', short_id) or len(short_id) > 16)
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if (
        short_id and
        URLMap.query.filter_by(short=short_id).first() is not None
    ):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    if not short_id:
        short_id = get_unique_short_id()

    new_link = URLMap(original=url, short=short_id)
    db.session.add(new_link)
    db.session.commit()
    short_url = url_for('index', _external=True) + short_id

    return jsonify({'url': url, 'short_link': short_url}), HTTPStatus.CREATED
