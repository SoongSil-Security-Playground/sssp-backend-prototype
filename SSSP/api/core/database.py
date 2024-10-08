from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SSSP.config import settings

# directory dependency

DATABASE_FILENAME = settings.database.filename
DATABASE_STORAGE = settings.database.storage
SQLALCHEMY_DATABASE_URL = settings.database.sqlite_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database Utils

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
