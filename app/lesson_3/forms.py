from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class RegisterForm(FlaskForm):
    first_name = StringField(
        "Имя",
        validators=[DataRequired(message="Поле обязательно")],
    )

    last_name = StringField(
        "Фамилия",
        validators=[DataRequired(message="Поле обязательно")],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Поле обязательно"),
            Email(message="email не является валидным адресом"),
        ],
    )
    birthday = DateField("Дата рождения")
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Поле обязательно"),
            Length(min=8, message="Должен состоять как минимум из 8 символов"),
            Regexp(
                "(?=.*[0-9])(?=.*[a-zA_Z])",
                message="Должен включать хотя бы одну букву и одну цифру",
            ),
        ],
        render_kw={
            "placeholder": "Пароль состоит из минимум 8 символов и должен включать хотя бы одну букву и одну цифру "
        },
    )
    password_confirm = PasswordField(
        "Подтверждение пароля",
        validators=[
            DataRequired(message="Поле обязательно"),
            EqualTo("password", message="Пароли не совпадают"),
        ],
    )
    agreement = BooleanField("Подтверждаю согласие на обработку персональных данных")
    register = SubmitField("Зарегистрироваться")
