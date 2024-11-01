from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO)

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users
from SSSP.api.core import auth
from SSSP.api.core.database import *

router = APIRouter()


@router.get("/user", response_model=schema_users.UserResponse)
def get_user(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    find_user = auth.get_current_user_by_jwt(token, db)
    logging.info(f"[*] GET_USER>> find user {find_user}")
    return schema_users.UserResponse.from_orm(find_user)
