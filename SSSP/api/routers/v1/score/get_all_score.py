from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.models.enums.user_role import UserRole

from SSSP.api.schemas import schema_score
from SSSP.api.core.database import *
from SSSP.api.core.auth import get_current_user_by_jwt

from SSSP.config import settings

import logging
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/score", response_model=list[schema_score.ScoreResponse])
def get_all_score(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    user = get_current_user_by_jwt(token, db)

    users = db.query(models.User).all()
    user_responses = []
    for user in users:
        if user.authority == UserRole.ADMIN:
            continue

        if user.username in settings.ban_info.ban_list:
            continue

        data = {
            'username':user.username,
            'total_score':calc_score(user, db)
        }
        user_responses.append(schema_score.ScoreResponse.construct(**data))
        
    logging.info(f"[*] Score List >> {user_responses}")

    return user_responses

def calc_score(user: models.User, db: Session):
    solved_list = user.solved_challenge
    score = 0
    for solve_id in solved_list:
        challenge = (
            db.query(models.Challenge).filter(models.Challenge.id == solve_id).first()
        )
        score += challenge.points

    return score
