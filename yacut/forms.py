from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional, Regexp, Length


class LinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Укажите исходную ссылку')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            # Для проверки допустимых символов имеет смысл использовать
            # регулярку. Или можно сделать кастомный валидатор и
            #переиспользовать его в АПИ
            Regexp(
                '^[a-zA-Z0-9]+$',
                message='В вашем варианте короткой ссылки использованы '
                        'недопустимые символы',
            ),
            # Поле должно быть опциональным
            Optional(),
            # Лучше использовать именованный параметр,
            # тогда нижнюю границу указывать не нужно
            Length(max=16)
        ])
    submit = SubmitField('Создать')
