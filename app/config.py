import secrets
import urllib.parse
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    HOST = '0.0.0.0'
    PORT = 8001
    PROJECT_NAME = "Catalog"
    API_V1_STR: str = "/api/v2/catalog"

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASES_URI: Optional[PostgresDsn] = None
    LOG_LEVEL = 'trace'

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: int

    @validator("SQLALCHEMY_DATABASES_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=urllib.parse.quote_plus(values.get("POSTGRES_PASSWORD")),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'

    class Config:
        env_file = "../.env"
        case_sensitive = True


settings = Settings()
