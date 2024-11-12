from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# directory dependency

from SSSP.config import settings

engine = create_engine(settings.database.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
