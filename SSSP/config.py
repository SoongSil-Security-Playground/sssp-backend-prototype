from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from typing import ClassVar
from datetime import datetime
from zoneinfo import ZoneInfo

import os

NOW = datetime.now(ZoneInfo("Asia/Seoul"))


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


class S3:
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


class Settings(BaseSettings):
    app_name: str = "Soongsil Security Playground"
    favicon_path: str = "./SSSP/static/favicon.ico"

    jwt: Jwt = Jwt()
    oauth2_scheme: ClassVar[OAuth2PasswordBearer] = OAuth2PasswordBearer(
        tokenUrl="/api/v1/auth/login"
    )
    database: Database = Database()


s3 = S3()
settings = Settings()
