from pydantic import BaseModel

class ScoreResponse(BaseModel):
    username: str
    total_score: int

    class Config:
        from_attributes=True