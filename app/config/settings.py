from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str


settings = Settings()
settings.database_url = str(settings.database_url)
