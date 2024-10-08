from pydantic_settings import BaseSettings

class Jwt():
    secret_key = "develop_key"
    algorithm = "HS256"
    token_expire_minutes = 30

class Database():
    filename = "test.db"
    storage = f'./SSSP/storag/{filename}'
    sqlite_url = f"sqlite:///{storage}"

class Settings(BaseSettings):
    app_name = "Soongsil Security Playground"
    favicon_path = './static/favicon.ico'
    
    jwt = Jwt()
    database = Database()

settings = Settings()