from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from SSSP.api.core.database import get_db
from SSSP.api.core.auth import get_current_user_by_jwt
from SSSP.api.models import models
from SSSP.api.models.enums.user_role import UserRole
from SSSP.api.schemas import schema_challenges
from SSSP.config import settings, s3
from SSSP.util.s3_client import s3_client

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.post("/{challenge_id}/submit")
def submit_challenge(
    challenge_id: int,
    flag: str = Form(None),
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    
    # Solver
    user = get_current_user_by_jwt(token, db)

    challenge = (
        db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    )

    if not challenge:
        logging.warning(f"Failed to find Challenge : {challenge_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found"
        )

    is_correct = challenge.flag == flag
    is_already_solve = False
    
    # TODO: Remove Race Window
    # 1. User1 - req
    #   2. User1 - req

    # 3. User1 Submission
    #   4. User1 Submission

    # Solution => recall get_current_user_by_jwt()
    
    is_already_solve = challenge.id in user.solved_challenge
    if is_already_solve:
        comment = "Already Solve!"

    else:
        if is_correct:
            comment = "Correct!"
        else:
            comment = "Wrong Flag!"

    if comment == "Correct!":
        # Challenge Commit for dynamic 
        if challenge.is_dynamic == True:
            minimum = challenge.minimum_points
            initial = challenge.initial_points
            decay   = challenge.decay
            solve_count = challenge.solve_count

            new_point = int((((minimum - initial) / (decay ** 2)) * (solve_count ** 2)) + initial)
            logging.info("New Dynamic Point! : " + str(new_point))
            challenge.points = new_point
        challenge.solve_count = challenge.solve_count + 1

        # User Commit
        user.solved_challenge = user.solved_challenge + [challenge_id]
        user.total_score = user.total_score + challenge.points

        # TODO: Rank Sorting 

    # Submission Commit
    logging.info("====== New Submission  ======")
    logging.info("Challenge Name : " + str(challenge.name))
    logging.info("Challenge Flag : " + challenge.flag)
    logging.info("Username       : " + str(user.username))
    logging.info("User      Flag : " + flag)

    new_submit = models.Submission(
        submitted_flag = challenge.flag,
        is_correct = is_correct,
        comment=comment,
        user_id = user.id,
        challenge_id = challenge.id,
        user = user,
        challenge = challenge,
    )

    db.add(new_submit)
    db.commit()
    db.refresh(user)
    db.refresh(new_submit)
    db.refresh(challenge)

    return {'detail': comment}
