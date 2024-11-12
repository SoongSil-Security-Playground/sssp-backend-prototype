# SSSP/api/schemas/schema_challenges.py

from pydantic import BaseModel
from datetime import datetime


class ChallengeResponse(BaseModel):
    id: int
    name: str
    description: str
    points: int
    created_at: datetime
    category_id: int

    class Config:
        orm_mode = True
        from_attributes = True
