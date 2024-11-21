from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from datetime import datetime 
from zoneinfo import ZoneInfo

# directory dependency
from SSSP.api.models.enums.user_role import UserRole
from SSSP.api.models.enums.challenge_category import ChallengeCategory

Base = declarative_base()


class User(Base):
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    contents = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now(ZoneInfo("Asia/Seoul")))
    authority = Column(SQLEnum(UserRole), default=UserRole.USER)

    rank = Column(Integer, nullable=True)
    solved_challenge = Column(JSON, default=list)

    # admin 이라면 notices 관리하니까 
    notices = relationship("Notice", back_populates="author")
    submissions = relationship("Submission", back_populates="user")

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    flag = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(ZoneInfo("Asia/Seoul")))
    category = Column(SQLEnum(ChallengeCategory), nullable=False)
    file_path = Column(String(255))
    points = Column(Integer, nullable=False)

    # Dynamic Scoring 적용했을 때 initial_point에서 minimum_point 까지 decay 적용하여 current point를 계산
    
    # 기본 처리 공식
    # value = (((minimum - initial) / (decay ** 2)) * (solve_count ** 2)) + initial
    # value = math.ceil(value)

    initial_points = Column(Integer, nullable=False)
    minimum_points = Column(Integer, nullable=False)
    decay = Column(Integer, nullable=False, default=100)
    is_dynamic = Column(Boolean, nullable=False)

    solve_count = Column(Integer, default=0)

    submissions = relationship("Submission", back_populates="challenge")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    submitted_flag = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(ZoneInfo("Asia/Seoul")))
    comment = Column(String(255), nullable=False)
    
    # Dynamic Scoring 적용했을 때, 해당 필드 켜서 각 제출에 대한 점수 계산 ( + 로깅 )
    # points_earned = Column(Float, nullable=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)

    user = relationship("User", back_populates="submissions")
    challenge = relationship("Challenge", back_populates="submissions")


class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(ZoneInfo("Asia/Seoul")))

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="notices")
