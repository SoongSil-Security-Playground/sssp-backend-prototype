from pydantic import BaseModel

class NoticeResponse(BaseModel):
    username: str
    total_score: int

    class Config:
        from_attributes=True