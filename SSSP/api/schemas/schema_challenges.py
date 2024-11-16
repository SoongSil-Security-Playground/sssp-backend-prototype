# schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# directory dependency
from SSSP.api.models.enums.challenge_category import ChallengeCategory


class ChallengeBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str
    points: int
    category: ChallengeCategory


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    points: Optional[int]
    category: Optional[ChallengeCategory]


class ChallengeResponse(ChallengeBase):
    id: int
    created_at: datetime
    file_path: Optional[str] = None

    class Config:
        from_attributes = True
