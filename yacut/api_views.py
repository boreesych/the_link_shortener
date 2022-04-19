import re
from datetime import datetime
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import Invalid_API_usage
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    link = URL_map.query.filter_by(short=short_id).first()
    if link is None:
        raise Invalid_API_usage(
        'Указанный id не найден',
        status_code=HTTPStatus.NOT_FOUND
    )
    return jsonify({'url': link.original}), HTTPStatus.OK
    


@app.route('/api/id/', methods=['POST'])
def create_id():
    if request.json is None:
        raise Invalid_API_usage('Отсутствует тело запроса')

    url = request.json.get('url')
    short_id = request.json.get('custom_id')

    if url is None:
        raise Invalid_API_usage('"url" является обязательным полем!')

    if short_id and (re.search(r'[^a-zA-Z0-9]', short_id) or len(short_id) > 16):
        raise Invalid_API_usage('Указано недопустимое имя для короткой ссылки')

    if short_id and URL_map.query.filter_by(short=short_id).first() is not None:
        raise Invalid_API_usage(f'Имя "{short_id}" уже занято.')

    if not short_id:
        short_id = get_unique_short_id()

    new_link = URL_map(original=url, short=short_id, timestamp=datetime.now())
    db.session.add(new_link)
    db.session.commit()
    short_url = url_for('index', _external=True) + short_id

    return jsonify({'url': url, 'short_link': short_url}), HTTPStatus.CREATED
