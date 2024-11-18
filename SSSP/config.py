from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from typing import ClassVar
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import Field

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


class InitialAdmin:
    def __init__(self):
        self.INITIAL_ADMIN_ID = os.getenv("INITIAL_ADMIN_ID", 'admin')
        self.INITIAL_ADMIN_PW = os.getenv("INITIAL_ADMIN_PW", 'admin')


class S3:
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST", "sssp_redis")
    REDIS_PORT: int = os.getenv("REDIS_PORT", "6379")


class EmailSettings(BaseSettings):
    sender_email: str = Field(default=None)
    sender_password: str = Field(default=None)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow",
    }


class Settings(BaseSettings):
    app_name: str = "Soongsil Security Playground"
    favicon_path: str = "./SSSP/static/favicon.ico"

    jwt: Jwt = Jwt()
    oauth2_scheme: ClassVar[OAuth2PasswordBearer] = OAuth2PasswordBearer(
        tokenUrl="/api/v1/auth/login"
    )
    database: Database = Database()
    initial_account: InitialAdmin = InitialAdmin()
    s3: S3 = S3()
    redis: RedisSettings = RedisSettings()
    email: EmailSettings = EmailSettings(
        sender_email=os.getenv("GOOGLE_EMAIL", "a"),
        sender_password=os.getenv("GOOGLE_EMAIL_SECRET", 'b'),
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow",
    }


s3 = S3()
settings = Settings()
