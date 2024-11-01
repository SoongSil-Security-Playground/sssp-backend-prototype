from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from typing import ClassVar


class Jwt:
    secret_key: str = "develop_key"
    algorithm: str = "HS256"
    token_expire_minutes: int = 30


class Database:
    filename: str = "test.db"
    storage: str = f"./SSSP/storage/{filename}"
    sqlite_url: str = f"sqlite:///{storage}"


class Settings(BaseSettings):
    app_name: str = "Soongsil Security Playground"
    favicon_path: str = "./static/favicon.ico"

    jwt: Jwt = Jwt()
    oauth2_scheme: ClassVar[OAuth2PasswordBearer] = OAuth2PasswordBearer(
        tokenUrl="/api/v1/auth/login"
    )
    database: Database = Database()


settings = Settings()
