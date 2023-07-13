from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    NAME_MAX_LENGTH: int = 50
    EMAIL_MAX_LENGTH: int = 128
    PASSWORD_MIN_LENGTH: int = 8

    class Config:
        env_file = "lesson_6/online-shop/.env"


settings = Settings()
