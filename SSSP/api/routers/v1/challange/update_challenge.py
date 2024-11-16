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


@router.patch("/{challenge_id}", response_model=schema_challenges.ChallengeResponse)
def update_challenge(
    challenge_id: int,
    name: str = Form(None),
    description: str = Form(None),
    points: int = Form(None),
    category: str = Form(None),
    file: UploadFile = File(None),
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

    if name is not None:
        challenge.name = name
    if description is not None:
        challenge.description = description
    if points is not None:
        challenge.points = points
    if category is not None:
        challenge.category = category

    if file:
        try:
            # 기존 파일 삭제
            if challenge.file_path:
                old_file_key = challenge.file_path.split(
                    f"https://{s3.S3_BUCKET_NAME}.s3.amazonaws.com/"
                )[-1]
                s3_client.delete_object(Bucket=s3.S3_BUCKET_NAME, Key=old_file_key)
                logging.info(f"Deleted old file from S3: {old_file_key}")

            file_key = f"challenges/{file.filename}"
            s3_client.put_object(
                Bucket=s3.S3_BUCKET_NAME,
                Key=file_key,
                Body=file.file,
                ContentType=file.content_type,
            )
            logging.info(f"File {file.filename} uploaded to S3 bucket")

            download_url = f"https://{s3.S3_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
            challenge.file_path = download_url
        except Exception as e:
            logging.error(f"Failed to upload file to S3 or generate URL: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload file or generate download URL",
            )

    db.commit()
    db.refresh(challenge)

    logging.info(f"[+] Challenge updated: {challenge}")
    return schema_challenges.ChallengeResponse.from_orm(challenge)
