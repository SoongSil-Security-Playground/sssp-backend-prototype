from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, timezone

# directory dependency
from SSSP.api.models.enums.user_role import UserRole
from SSSP.api.models.enums.challenge_category import ChallengeCategory
from SSSP.config import NOW


Base = declarative_base()


class User(Base):
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)  # 길이 지정
    email = Column(String(255), unique=True, index=True)  # 길이 지정
    hashed_password = Column(String(255))  # 길이 지정
    contents = Column(String(500), nullable=True)  # 길이 지정
    created_at = Column(DateTime, default=NOW)
    authority = Column(SQLEnum(UserRole), default=UserRole.USER)

    notices = relationship("Notice", back_populates="author")
    submissions = relationship("Submission", back_populates="user")


class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    points = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=NOW)
    category = Column(SQLEnum(ChallengeCategory), nullable=False)
    file_path = Column(String(255))

    submissions = relationship("Submission", back_populates="challenge")


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    submitted_flag = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=NOW)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)

    user = relationship("User", back_populates="submissions")
    challenge = relationship("Challenge", back_populates="submissions")


class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=NOW)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="notices")
