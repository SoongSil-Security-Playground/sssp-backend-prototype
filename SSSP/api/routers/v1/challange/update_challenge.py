from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.core.database import get_db
from SSSP.api.core.auth import get_current_user_by_jwt
from SSSP.api.models import models
from SSSP.api.models.enums.user_role import UserRole
from SSSP.api.schemas import schema_challenges
from SSSP.config import settings

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.put("/{challenge_id}", response_model=schema_challenges.ChallengeResponse)
def update_challenge(
    challenge_id: int,
    challenge_update: schema_challenges.ChallengeUpdate,
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = get_current_user_by_jwt(token, db)

    if user.authority != UserRole.ADMIN:
        logging.warning(f"Unauthorized attempt to update challenge by user {user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update challenges",
        )

    challenge = (
        db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    )
    if not challenge:
        logging.warning(f"Challenge not found for update: ID {challenge_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found"
        )

    if challenge_update.name is not None:
        challenge.name = challenge_update.name
    if challenge_update.description is not None:
        challenge.description = challenge_update.description
    if challenge_update.points is not None:
        challenge.points = challenge_update.points
    if challenge_update.category is not None:
        challenge.category = challenge_update.category

    db.commit()
    db.refresh(challenge)

    logging.info(f"[+] Challenge updated: {challenge}")
    return schema_challenges.ChallengeResponse.from_orm(challenge)
