from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    contents: str


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    contents: str

    class Config:
        from_attributes = True
