from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    secret_key: SecretStr
    algorithm: str = "HS256"

    database_url: str
    expire_time_in_mins: int = 5
    refresh_token_duration_in_days: int


settings = Setting()  # type: ignore
