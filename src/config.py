from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    base_url: str