# SSSP/api/routers/get_challenges.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from SSSP.api.models import models
from SSSP.api.schemas import schema_challenges
from SSSP.api.core.database import get_db
from SSSP.config import settings

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/challenges", response_model=list[schema_challenges.ChallengeResponse])
def get_challenges(
    token: str = Depends(settings.oauth2_scheme), db: Session = Depends(get_db)
):
    challenges = db.query(models.Challenge).all()
    challenge_responses = [
        schema_challenges.ChallengeResponse.from_orm(challenge)
        for challenge in challenges
    ]
    logging.info(f"[*] CHALLENGE_LIST>> {challenge_responses}")
    return challenge_responses
