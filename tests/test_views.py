from yacut.models import URL_map


def test_index_form_get(client):
    got = client.get('/')
    assert got.status_code == 200
    assert b"form" in got.data, (
        'Добавьте форму в конекст страницы `index`'
    )


def test_index_form_post(client):
    got = client.post('/', data={
        'original_link': 'https://www.python.org',
        'custom_id': 'py',
    })
    assert got.status_code == 200, (
        'Главная страница при отправке формы должна возвращать статус 200'
    )
    unique_id = URL_map.query.filter_by(original='https://www.python.org', short='py').first()
    assert unique_id, (
        'Главная страница при отправке формы должна создавать в базе данных запись'
    )
    assert '<a href="http://localhost/py"' in got.data.decode('utf-8'), (
        'На главной странице при отправке формы должная возвращаться новая ссылка'
    )


def test_duplicated_url_in_form(client, short_python_url):
    got = client.post('/', data={
        'original_link': 'https://www.python.org',
        'custom_id': 'py',
    }, follow_redirects=True)
    assert 'Имя py уже занято!' in got.data.decode('utf-8'), (
        'При использовании уже занятой короткой ссылки на странице должен '
        'отображаться текст "Имя <short_name> уже занято!"'
    )

def test_get_unique_short_id(client):
    got = client.post('/', data={
        'original_link': 'https://www.python.org',
    })
    assert got.status_code == 200, (
        'Главная страница при отправке формы без заданного значения короткой ссылки '
        'должна возвращать статус 200'
    )
    unique_id = URL_map.query.filter_by(original='https://www.python.org').first()
    assert unique_id, (
        'Главная страница при отправке формы без заданного значения короткой ссылки '
        'должна создавать в базе данных запись'
    )
    assert f'Ваша новая ссылку готова: http://localhost:5000/{unique_id.short}'


def test_redirect_url(client, short_python_url):
    got = client.get(f'/{short_python_url.short}')
    assert got.status_code == 302, (
        'При перенаправлении по короткому адресу убедитесь что возвращается статус 302'
    )
    assert got.location == short_python_url.original, (
        'При перенаправлении по короткому адресу убедитесь в корректности оригинального адреса'
    )
