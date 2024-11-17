from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_score
from SSSP.api.core.database import *
from SSSP.api.core.auth import get_current_user_by_jwt

import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/score", response_model=list[schema_score.ScoreResponse])
def get_all_score(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    user = get_current_user_by_jwt(token, db)

    users = db.query(models.User).all()
    user_responses = [schema_score.ScoreResponse.from_orm(user) for user in users]
    logging.info(f"[*] Score List >> {user_responses}")

    return user_responses