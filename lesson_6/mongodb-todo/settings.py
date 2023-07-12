from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_NAME: str

    TITLE_MIN_LENGTH: int = 2
    TITLE_MAX_LENGTH: int = 128
    DESCRIPTION_MAX_LENGTH: int = 256

    class Config:
        env_file = "lesson_6/mongodb-todo/.env"


settings = Settings()
