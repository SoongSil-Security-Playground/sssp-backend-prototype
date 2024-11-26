from pydantic import BaseModel

class LogResponse(BaseModel):
    id: int
    user_id: int
    comment: str
    submitted_flag: str

    class Config:
        from_attributes = True

