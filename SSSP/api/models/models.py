from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# directory dependency

Base = declarative_base()


class User(Base):
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    contents = Column(String)
