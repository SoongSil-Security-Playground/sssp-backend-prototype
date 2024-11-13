from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
import logging

logging.basicConfig(level=logging.INFO)

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users
from SSSP.api.core import auth
from SSSP.api.core.database import *
from SSSP.config import settings

router = APIRouter()


@router.get("/auth-check")
def auth_check(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    logging.info(f"[*] TOKEN: {token}")
    get_user = auth.get_current_user_by_jwt(token, db)
    logging.info(f"[*] userinfo {get_user}")
    return {"authority": get_user.authority}
