from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp


class AnswerForm(FlaskForm):
    word = StringField("Введите ответ", [InputRequired(message="Заполните поле"),
                                         Length(min=1, max=50),
                                         Regexp("^[a-zA-Z\s]+$")]
                       )
    submit = SubmitField("Проверить")
