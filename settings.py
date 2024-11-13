from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    FATHER_TOKEN: str = "FWGGWEJFOWEFJWEJFQWFQW;JFF"
    GITHUB_URL: str = "https://github.com/username/repository"


bot_settings = BotSettings()
