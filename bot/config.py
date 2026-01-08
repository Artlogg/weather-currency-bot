from pydantic import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="ignore",
    )


settings = Settings()
