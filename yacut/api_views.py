import re
from datetime import datetime

from flask import abort, jsonify, make_response, request, url_for

from yacut import app, db
from yacut.error_handlers import Invalid_API_usage
from yacut.models import URL_map
from yacut.views import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    link = URL_map.query.filter_by(short=short_id).first()
    if link:
        return jsonify({'url': link.original}), 200
    raise Invalid_API_usage('Указанный id не найден', status_code=404)


@app.route('/api/id/', methods=['POST'])
def create_id():
    if not request.json:
        raise Invalid_API_usage('Отсутствует тело запроса')

    url = request.json.get('url')
    short_id = request.json.get('custom_id')

    if short_id and re.search(r'[^a-zA-Z0-9]', short_id):
        raise Invalid_API_usage('Указано недопустимое имя для короткой ссылки')

    if short_id and URL_map.query.filter_by(short=short_id).first() is not None:
        message = f'Имя "{short_id}" уже занято.'
        raise Invalid_API_usage(message)

    if url is None:
        message = '"url" является обязательным полем!'
        raise Invalid_API_usage(message)

    if short_id is None or short_id == '':
        short_id = get_unique_short_id()

    new_link = URL_map(original=url, short=short_id, timestamp=datetime.now())
    db.session.add(new_link)
    db.session.commit()
    short_url = url_for('index', _external=True) + short_id

    return jsonify({'url': url, 'short_link': short_url}), 201
