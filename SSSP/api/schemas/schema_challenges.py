# schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# directory dependency

class ChallengeBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str
    points: int
    category: str

class ChallengeUpdate(ChallengeBase):
    file_path: Optional[str] = None

class ChallengeResponse(ChallengeBase):
    id: int
    created_at: datetime
    file_path: Optional[str] = None
    category: str
    is_user_solved: Optional[int] = None
    solve_count: int
    
    class Config:
        from_attributes = True
