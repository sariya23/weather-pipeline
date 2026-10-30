from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_url: str = Field(validation_alias="BASE_URL")
    host: str = Field(validation_alias="POSTGRES_HOST")
    port: int = Field(validation_alias="POSTGRES_PORT")
    user: str = Field(validation_alias="POSTGRES_USER")
    password: SecretStr = Field(validation_alias="POSTGRES_PASSWORD")
    name: str = Field(validation_alias="POSTGRES_NAME")
    ssl_mode: str = Field(validation_alias="POSTGRES_SSL_MODE")

    postgres_outer_host: str = Field(validation_alias="POSTGRES_OUTER_HOST")
