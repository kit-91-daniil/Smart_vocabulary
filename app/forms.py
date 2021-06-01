from wtforms import Form, StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import EqualTo, InputRequired, Length
from flask_security.forms import LoginForm, _default_field_labels, \
    get_form_field_label, Required, password_required


class MyCustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)

    _default_field_labels["email"] = "Email"
    _default_field_labels["password"] = "Пароль"
    _default_field_labels["remember_me"] = "Запомнить меня"
    _default_field_labels["login"] = "Войти"
    email = StringField(get_form_field_label("email"),
                        validators=[Required(message="EMAIL_NOT_PROVIDED")])
    password = PasswordField(get_form_field_label('password'),
                             validators=[password_required])
    remember = BooleanField(get_form_field_label('remember_me'))
    submit = SubmitField(get_form_field_label('login'))


class MyRegisterForm(Form):
    name = StringField("Имя", [InputRequired(message="Insert name"), Length(min=1, max=20)])
    email = StringField("email", [InputRequired(message="Insert login"), Length(min=3, max=20)])
    password = PasswordField("Пароль", [InputRequired(message="Input password"),
                                        EqualTo("confirm", message="Password must match"),
                                        Length(min=4, max=20)])
    confirm = PasswordField("Повторите пароль", [InputRequired(message="Repeat your password, please.")])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Регистрация")
