from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_DB: str = "casino_db"
    POSTGRES_USER: str = "casino_user"
    POSTGRES_PASSWORD: str = "casino_password"
    DATABASE_URL: PostgresDsn
    DATABASE_ECHO: bool = False

    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Redis
    REDIS_URL: RedisDsn
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Возвращает URL базы данных в виде строки для SQLAlchemy / Asyncpg."""
        return str(self.DATABASE_URL)


settings = Settings()