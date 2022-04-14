import string
from datetime import datetime
from random import choice

from flask import abort, flash, redirect, render_template, url_for

from . import ID_LENGHT, app, db
from .forms import LinkForm
from .models import URL_map


def get_short_id(number):
    generated_id = [
        choice(string.ascii_letters + string.digits) for _ in range(number)
        ]
    return ''.join(generated_id)


def get_unique_short_id():
    new_id = get_short_id(ID_LENGHT)
    while URL_map.query.filter_by(short=new_id).first():
        new_id = get_short_id(ID_LENGHT)
    return new_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LinkForm()
    if form.validate_on_submit():
        url = form.original_link.data
        short_id = form.custom_id.data

        if (
            short_id and
            URL_map.query.filter_by(short=short_id).first()
        ):
            flash(f'Имя {short_id} уже занято!')
            return redirect(url_for('index'))

        if not short_id:
            short_id = get_unique_short_id()

        new_link = URL_map(
            original=url, 
            short=short_id,
            timestamp=datetime.now()
            )
        db.session.add(new_link)
        db.session.commit()
        short_url = url_for('index', _external=True) + short_id

        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_url(short_id):
    link = URL_map.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)