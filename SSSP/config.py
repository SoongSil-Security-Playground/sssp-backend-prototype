from pydantic_settings import BaseSettings

class Jwt():
    secret_key : str = "develop_key"
    algorithm : str = "HS256"
    token_expire_minutes : int = 30

class Database():
    filename : str = "test.db"
    storage : str = f'./SSSP/storage/{filename}'
    sqlite_url : str = f"sqlite:///{storage}"

class Settings(BaseSettings):
    app_name : str = "Soongsil Security Playground"
    favicon_path : str = './static/favicon.ico'

    jwt : Jwt = Jwt()
    database : Database = Database()

settings = Settings()