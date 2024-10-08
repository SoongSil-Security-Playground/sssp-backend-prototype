from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_users

from SSSP.api.core.database import get_db

router = APIRouter()
@router.get("/user_list", response_model=list[schema_users.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users