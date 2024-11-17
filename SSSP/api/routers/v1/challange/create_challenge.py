from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from SSSP.api.core.database import get_db
from SSSP.api.core.auth import get_current_user_by_jwt
from SSSP.api.models import models
from SSSP.api.models.enums.user_role import UserRole
from SSSP.api.schemas import schema_challenges
from SSSP.config import settings, s3
from SSSP.util.s3_client import s3_client
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.post(
    "/",
    response_model=schema_challenges.ChallengeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_challenge(
    name: str = Form(...),
    description: str = Form(...),
    points: int = Form(...),
    category: str = Form(...),
    file: Optional[UploadFile] = File(None),
    flag: str = Form(...),
    decay: int = Form(None),
    minimum_point: Optional[int] = Form(None),
    is_dynamic: Optional[bool] = Form(None),
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = get_current_user_by_jwt(token, db)
    if user.authority != UserRole.ADMIN:
        logging.warning(f"Unauthorized attempt to create challenge by user {user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create challenges",
        )

    # S3 bucket generator for attachment
    download_url = None
    if file is not None:
        try:
            file_key = f"challenges/{file.filename}"
            s3_client.put_object(
                Bucket=s3.S3_BUCKET_NAME,
                Key=file_key,
                Body=file.file,
                ContentType=file.content_type,
            )
            logging.info(f"File {file.filename} uploaded to S3 bucket")

            download_url = f"https://{s3.S3_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
        except Exception as e:
            logging.error(f"Failed to upload file to S3 or generate URL: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload file or generate download URL",
            )
    else:
        # if file is not required.
        download_url = None

    db_challenge = models.Challenge(
        name=name,
        description=description,
        points=points,
        category=category,
        file_path=download_url,
        flag=flag,

        decay=decay,
        initial_points=points,
        minimum_points=minimum_point,
        is_dynamic=is_dynamic,
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)

    logging.info(f"[+] Challenge created: {db_challenge}")

    return schema_challenges.ChallengeResponse.from_orm(db_challenge)
