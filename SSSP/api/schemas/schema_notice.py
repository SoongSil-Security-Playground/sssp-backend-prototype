from pydantic import BaseModel
from datetime import datetime


class NoticeResponse(BaseModel):
    title: str
    content: str
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
