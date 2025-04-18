from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users
from SSSP.api.core import auth
from SSSP.api.core.database import *

router = APIRouter()


@router.post("/register", response_model=schema_users.UserResponse)
def register(request: schema_users.UserCreateRequest, db: Session = Depends(get_db)):
    user_in_db = (
        db.query(models.User).filter(models.User.email == request.email).first()
    )
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_in_auth_list = (
        db.query(models.AuthUserList).filter(models.AuthUserList.useremail == request.email).first()
    )

    if not user_in_auth_list:
        raise HTTPException(status_code=400, detail="Please verify your email first.")

    hashed_password = auth.get_password_hash(request.password)

    new_user = models.User(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        contents="",
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return schema_users.UserResponse.from_orm(new_user)
