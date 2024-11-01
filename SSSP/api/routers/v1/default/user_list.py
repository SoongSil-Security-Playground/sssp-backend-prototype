from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO)

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users
from SSSP.api.core.database import *

router = APIRouter()


@router.get("/user_list", response_model=list[schema_users.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    logging.info(f"[*] USER_LIST>> {users}")
    return users
