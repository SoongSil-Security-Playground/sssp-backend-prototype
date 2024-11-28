from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from SSSP.api.models import models
from SSSP.api.schemas import schema_score
from SSSP.api.core.database import get_db
from SSSP.api.core.auth import get_current_user_by_jwt
from SSSP.config import settings

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/me", response_model=schema_score.ScoreResponse)
def get_my_score(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    user = get_current_user_by_jwt(token, db)

    data = {"username": user.username, "total_score": calc_score(user, db)}

    response = schema_score.ScoreResponse.construct(**data)
    logging.info(f"[*] My Score >> {response}")

    return response


def calc_score(user: models.User, db: Session):
    solved_list = user.solved_challenge
    score = 0
    for solve_id in solved_list:
        challenge = (
            db.query(models.Challenge).filter(models.Challenge.id == solve_id).first()
        )
        score += challenge.points

    return score
