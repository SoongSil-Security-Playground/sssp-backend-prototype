from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from datetime import datetime

# directory dependency
from SSSP.api.models.enums.user_role import UserRole

Base = declarative_base()


class User(Base):
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    contents = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    authority = Column(SQLEnum(UserRole), default=UserRole.USER)
    # 관계 설정: 공지사항들
    notices = relationship("Notice", back_populates="author")
    # 관계 설정: 제출들
    submissions = relationship("Submission", back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    # 기본 키
    id = Column(Integer, primary_key=True, index=True)
    # 카테고리 이름
    name = Column(String, unique=True, nullable=False)
    # 생성 일자
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정: 문제들
    challenges = relationship("Challenge", back_populates="category")


class Challenge(Base):
    __tablename__ = "challenges"
    # 기본 키
    id = Column(Integer, primary_key=True, index=True)
    # 문제 이름
    name = Column(String, nullable=False)
    # 문제 설명
    description = Column(Text, nullable=False)
    # 배점
    points = Column(Integer, nullable=False)
    # 생성 일자
    created_at = Column(DateTime, default=datetime.utcnow)

    # 카테고리 외래 키
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    # 관계 설정: 카테고리
    category = relationship("Category", back_populates="challenges")
    # 관계 설정: 첨부파일들
    attachments = relationship("Attachment", back_populates="challenge")
    # 관계 설정: 제출들
    submissions = relationship("Submission", back_populates="challenge")


class Attachment(Base):
    __tablename__ = "attachments"
    # 기본 키
    id = Column(Integer, primary_key=True, index=True)
    # 파일 경로 또는 URL
    file_path = Column(String, nullable=False)
    # 생성 일자
    created_at = Column(DateTime, default=datetime.utcnow)

    # 문제 외래 키
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    # 관계 설정: 문제
    challenge = relationship("Challenge", back_populates="attachments")


class Submission(Base):
    __tablename__ = "submissions"
    # 기본 키
    id = Column(Integer, primary_key=True, index=True)
    # 제출한 플래그
    submitted_flag = Column(String, nullable=False)
    # 정답 여부
    is_correct = Column(Boolean, default=False)
    # 생성 일자
    created_at = Column(DateTime, default=datetime.utcnow)

    # 유저 외래 키
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 문제 외래 키
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    # 관계 설정: 유저
    user = relationship("User", back_populates="submissions")
    # 관계 설정: 문제
    challenge = relationship("Challenge", back_populates="submissions")


class Notice(Base):
    __tablename__ = "notices"
    # 기본 키
    id = Column(Integer, primary_key=True, index=True)
    # 제목
    title = Column(String, nullable=False)
    # 내용
    content = Column(Text, nullable=False)
    # 생성 일자
    created_at = Column(DateTime, default=datetime.utcnow)

    # 작성자 외래 키
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 관계 설정: 작성자
    author = relationship("User", back_populates="notices")
