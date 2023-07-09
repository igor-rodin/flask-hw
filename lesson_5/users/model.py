import uuid
from pydantic import BaseModel, EmailStr, Field, field_validator
from bcrypt import hashpw, checkpw, gensalt


class UserOut(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    email: EmailStr = Field(..., description="Email пользователя")


class UserIn(UserOut):
    password: str = Field(..., description="Пароль пользователя")

    @field_validator("password")
    def validate_pwd(cls, value):
        if len(value) < 8:
            raise ValueError(
                "Пароль пользователя, должен содержать как минимум 8 символов"
            )
        if (
            not any(map(str.isdigit, value))
            or not any(map(str.islower, value))
            or not any(map(str.isupper, value))
        ):
            raise ValueError(
                "Пароль пользователя, должен содержать символы в верхнем и нижнем регистрах и цифры"
            )
        return value


class User(UserOut):
    id: uuid.UUID = uuid.uuid4()

    password_hash: str

    def set_password(self, password: str) -> str:
        salt = gensalt()
        self.password_hash = hashpw(
            salt=salt, password=password.encode("utf-8")
        ).decode("utf-8")

    def is_valid_password(self, password: str) -> bool:
        return checkpw(
            password.encode("utf-8"), hashed_password=self.password_hash.encode("utf-8")
        )


if __name__ == "__main__":
    u = User(
        name="Me",
        email="u2mail@mail.ru",
        password_hash="uytiuyt987598yufjk",
        password="sJfjhgfg3hjhgfjh",
    )
