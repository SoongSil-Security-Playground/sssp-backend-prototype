from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users
from SSSP.api.core import auth

from SSSP.api.core.database import *

router = APIRouter()


@router.post("/register", response_model=schema_users.User)
def register(user: schema_users.UserCreate, db: Session = Depends(get_db)):
    user_in_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        contents=user.contents,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
