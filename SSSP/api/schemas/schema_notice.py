from pydantic import BaseModel

class NoticeResponse(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes=True