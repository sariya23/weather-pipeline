from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    base_url: str
    host: str
    port: int
    user: str
    password: SecretStr
    name: str
    ssl_mode: str