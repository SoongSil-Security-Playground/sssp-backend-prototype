from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO)

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users
from SSSP.api.core.database import *
from SSSP.api.core.auth import get_current_user_by_jwt

router = APIRouter()

@router.get("/user_list", response_model=list[schema_users.UserResponse])
def get_user_list(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    user = get_current_user_by_jwt(token, db)
    users = db.query(models.User).all()
    user_responses = [schema_users.UserResponse.from_orm(user) for user in users]
    logging.info(f"[*] USER_LIST>> {user_responses}")
    return user_responses
