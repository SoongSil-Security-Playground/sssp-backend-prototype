from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoticeResponse(BaseModel):
    title: str
    content: str
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
