from shorts_app.models import URL_map

py_url = 'https://www.python.org'


def test_create_id(client):
    got = client.post('/api/id/', json={
        'url': py_url,
        'short_link': 'py',
    })
    assert got.status_code == 201, 'Статус ответа при создании короткой ссылки должен быть 201'
    assert list(got.json.keys()) == ['short_link', 'url'], (
        'При создании короткой ссылки в ответе должны быть ключи `url, short_link`'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/py',
    }, 'Тело ответа API отличается от ожидаемого при создании короткой ссылки'


def test_create_empty_body(client):
    got = client.post('/api/id/')
    assert got.status_code == 400, (
        'При пустом теле запроса для создании короткой ссылки статус ответа должен быть 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'При пустом теле запрос для создании короткой ссылки в ответе должен быть ключ `message`'
    )
    assert got.json == {'message': 'Отсутствует тело запроса'}, (
        'Сообщение в теле ответа при создании короткой ссылки '
        'без тела в запросе не соответствует спецификации'
    )


def test_invalid_short_url(client):
    got = client.post('/api/id/', json={
        'url': py_url,
        'short_link': '$',
    })
    assert got.status_code == 400, (
        'При недопустимом имени для короткой ссылки статус ответа должен быть 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'При недопустимом имени для короткой ссылки в ответе должен быть ключ `message`'
    )
    assert got.json == {'message': 'Указано недопустимое имя для короткой ссылки'}, (
        'Сообщение в теле ответа при недопустимом имени короткой ссылки '
        'в запросе не соответствует спецификации'
    )


def test_no_required_field(client):
    got = client.post('/api/id/', json={
        'short_link': 'python',
    })
    assert got.status_code == 400, (
        'При некорректном теле запроса для создании короткой ссылки статус ответа должен быть 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'При некорректном теле запроса для создании короткой ссылки в ответе должен быть ключ `message`'
    )
    assert got.json == {'message': '\"url\" является обязательным полем!'}, (
        'Сообщение в теле ответа при некорректном теле запроса '
        'не соответствует спецификации'
    )


def test_url_already_exists(client, short_python_url):
    got = client.post('/api/id/', json={
        'url': py_url,
        'short_link': 'py',
    })
    assert got.status_code == 400, (
        'При создании ссылки с коротким именем которое уже занято статус ответа должен быть 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'При создании ссылки с коротким именем которое уже занято в ответе должен быть ключ `message`'
    )
    assert got.json == {'message': 'Имя "py" уже занято.'}, (
        'Сообщение в теле ответа при создании ссылки с коротким именем которое уже занято '
        'не соответствует спецификации'
    )


def test_generated_unique_short_id(client):
    got = client.post('/api/id/', json={
        'url': py_url,
        'short_link': None,
    })
    assert got.status_code == 201, (
        'Статус ответа при создании короткой ссылки '
        'без явного указать имени короткой ссылки должен быть 201'
    )
    unique_id = URL_map.query.filter_by(original=py_url).first()
    assert unique_id, (
        'При создании ссылки без явного указания короткой ссылки '
        'должна генерироваться часть ссылки состоящая из '
        'символов в lowercase и цифр и сохраняться в базе данных'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/' + unique_id.short,
    }, (
        'При создании ссылки без явного указания короткой ссылки '
        'должна генерироваться часть ссылки состоящая из '
        'символов в lowercase и цифр и возвращаться в ответе API'
    )


def test_get_url_endpoint(client, short_python_url):
    got = client.get(f'/api/id/{short_python_url.short}/')
    assert got.status_code == 200, (
        'При GET запросе для получения ссылки статус ответа должен быть 200'
    )
    assert list(got.json.keys()) == ['url'], (
        'При GET запросе для получения ссылки в теле ответа должен быть ключ `url`'
    )
    assert got.json == {'url': py_url}, (
        'При GET запросе для получения ссылки тело ответа '
        'не соответствует спецификации'
    )


def test_get_url_not_fount(client):
    got = client.get('/api/id/{enexpected}/')
    assert got.status_code == 404, (
        'При GET запросе для получения ссылки которого не существует '
        'статус ответа должен быть 404'
    )
    assert list(got.json.keys()) == ['message'], (
        'При GET запросе для получения ссылки которого не существует в ответе должен быть ключ `message`'
    )
    assert got.json == {'message': 'Указанный id не найден'}, (
        'При GET запросе для получения ссылки которого не существует тело ответа '
        'не соответствует спецификации'
    )
