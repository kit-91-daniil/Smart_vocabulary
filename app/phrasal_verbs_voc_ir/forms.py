from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp


class PhrasalVerbAddInputForm(FlaskForm):
    phrasal_verb = StringField("Слово для перевода",
                               validators=[Length(min=1, max=40),
                                           InputRequired(message="Заполните поле"),
                                           Regexp("^[a-zA-Z\s]+$")]
                               )
    submit = SubmitField("Ввести")


class PhrasalVerbDeleteInputForm(FlaskForm):
    phrasal_verb = StringField("Слово для удаления",
                               validators=[InputRequired(message="Заполните поле"),
                                           Length(min=1, max=40),
                                           Regexp("^[a-zA-Z\s]+$")]
                               )
    submit = SubmitField("Ввести")


class SearchPhrasalVerbForm(FlaskForm):
    phrasal_verb = StringField("Слово для поиска",
                               validators=[InputRequired(message="Заполните поле"),
                                           Length(min=1, max=40),
                                           Regexp("^[a-zA-Z\s]+$")]
                               )
    submit = SubmitField("Ввести")
