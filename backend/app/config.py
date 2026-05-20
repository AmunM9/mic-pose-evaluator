from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://micpose:micpose_dev@localhost:5432/micpose"
    OPENAI_API_KEY: str
    ENVIRONMENT: str = "development"
    MAX_AUDIO_SIZE_MB: int = 25


settings = Settings()
