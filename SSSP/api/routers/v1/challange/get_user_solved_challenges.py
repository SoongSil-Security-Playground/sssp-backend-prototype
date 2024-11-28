from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.schemas import schema_challenges
from SSSP.api.core.database import get_db
from SSSP.api.core.auth import get_current_user_by_jwt
from SSSP.config import settings

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/solved/me", response_model=list[schema_challenges.ChallengeResponse])
def get_user_solved_challenges(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    user = get_current_user_by_jwt(token, db)
    user_solved_challenge_ids = user.solved_challenge

    solved_challenges = (
        db.query(models.Challenge)
        .filter(models.Challenge.id.in_(user_solved_challenge_ids))
        .all()
    )

    challenge_responses = []
    for challenge in solved_challenges:
        temp = schema_challenges.ChallengeResponse.from_orm(challenge)
        temp.is_user_solved = 1  # 이미 푼 문제이므로 1로 설정
        challenge_responses.append(temp)

    logging.info(f"[*] USER_SOLVED_CHALLENGES>> {challenge_responses}")
    return challenge_responses
