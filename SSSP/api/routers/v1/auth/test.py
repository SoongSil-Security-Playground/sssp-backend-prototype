from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

# directory dependency
from SSSP.api.models import models
from SSSP.api.core import auth
import logging
from SSSP.api.core.database import *
from SSSP.config import settings

router = APIRouter()


@router.get("/auth-check")
def auth_check(token: str = Depends(settings.oauth2_scheme)):
    logging.info(f"[*] TOKEN: {token}")
    return "AUTHENTICATED USER"
