from pydantic import BaseModel

class ScoreResponse(BaseModel):
    username: str
    total_score: float

    class Config:
        from_attributes=True