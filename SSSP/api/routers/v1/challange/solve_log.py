from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# directory dependency
from SSSP.api.models import models
from SSSP.api.core.database import get_db

import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.get("/sdijvoauv2398u98wqruwojfeihjfdbj82du9gv8h")
def solve_log(
    db: Session = Depends(get_db)
):
    solve_log = db.query(models.Submission).all()
    chall_db = db.query(models.Challenge).all()
    user_db = db.query(models.User).all()

    chall_dict = {chall.id: chall.name for chall in chall_db}
    flag_dict = {chall.id: chall.flag for chall in chall_db}
    user_dict = {user.id: user.username for user in user_db}

    response = list()

    for log in solve_log:
        chall_name = chall_dict.get(log.challenge_id, "Unknown Challenge")
        flag = flag_dict.get(log.challenge_id, "Unknown flag")
        username = user_dict.get(log.user_id, "Unknown User")
        comment = log.comment
        response.append({'chall' : chall_name, "username" : username, "comment":comment, "user_flag":log.submitted_flag, "real_flag": flag})

    return response[::-1]
