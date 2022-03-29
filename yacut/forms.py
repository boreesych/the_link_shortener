from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Optional, Regexp)


class LinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Укажите исходную ссылку')],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Regexp('[a-zA-Z0-9]',
            message='В вашем варианте короткой ссылки использованы недопустимые символы'),
            Optional(),
        ]
    )
    submit = SubmitField('Создать')
