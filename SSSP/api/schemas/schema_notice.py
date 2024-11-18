from pydantic import BaseModel

class NoticeResponse(BaseModel):
    title: str
    content: str
    id: int

    class Config:
        from_attributes=True