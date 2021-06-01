from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import EqualTo, InputRequired, Length, Regexp


class WordAddInputForm(FlaskForm):
    word = StringField("Слово для перевода",
                       validators=[Length(min=1, max=40),
                                   InputRequired(message="Заполните поле"),
                                   Regexp("^[a-zA-Z\s]+$")]
                       )
    submit = SubmitField("Ввести")


class WordDeleteInputForm(FlaskForm):
    word = StringField("Слово для удаления",
                       validators=[InputRequired(message="Заполните поле"),
                                   Length(min=1, max=40),
                                   Regexp("^[a-zA-Z\s]+$")]
                       )
    submit = SubmitField("Ввести")


class SearchWordForm(FlaskForm):
    word = StringField("Слово для поиска",
                       validators=[InputRequired(message="Заполните поле"),
                                   Length(min=1, max=40),
                                   Regexp("^[a-zA-Z\s]+$")]
                       )
    submit = SubmitField("Ввести")
