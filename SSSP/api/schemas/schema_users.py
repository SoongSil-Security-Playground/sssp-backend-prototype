from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    contents: str
    authority: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    contents: Optional[str] = None
    authority: str

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    contents: Optional[str] = None

    class Config:
        orm_mode = True
