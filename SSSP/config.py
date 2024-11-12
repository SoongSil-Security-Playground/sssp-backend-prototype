from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from typing import ClassVar
import os


class Jwt:
    secret_key: str = os.getenv("JWT_SECRET_KEY", "develop_key")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    token_expire_minutes: int = os.getenv("JWT_TOKEN_EXPIRE_MINUTES", "30")


class Database:
    def __init__(self):
        self.MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
        self.MYSQL_DB = os.getenv("MYSQL_DB", "sssp_database")
        self.MYSQL_USER = os.getenv("MYSQL_USER", "sssp")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "sssppassword")
        self.MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
        self.DATABASE_URL = f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"


class Settings(BaseSettings):
    app_name: str = "Soongsil Security Playground"
    favicon_path: str = "./SSSP/static/favicon.ico"

    jwt: Jwt = Jwt()
    oauth2_scheme: ClassVar[OAuth2PasswordBearer] = OAuth2PasswordBearer(
        tokenUrl="/api/v1/auth/login"
    )
    database: Database = Database()


settings = Settings()
