from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
import logging

logging.basicConfig(level=logging.INFO)

# directory dependency
from SSSP.api.models import models
from SSSP.api.core import auth
from SSSP.api.core.database import *
from SSSP.config import settings

router = APIRouter()


@router.get("/health-check")
def auth_check():
    return {"status": "healthy"}
