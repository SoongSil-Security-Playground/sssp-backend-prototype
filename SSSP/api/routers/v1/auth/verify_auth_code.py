from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from SSSP.api.core.database import get_db
from SSSP.api.models import models


from redis import Redis
import redis
import logging

from SSSP.api.core.redis import get_redis, get_auth_key

router = APIRouter()


@router.post("/verify-auth-code")
async def verify_auth_code(
    email: str,
    auth_code: str,
    redis_client: Redis = Depends(get_redis),
    db: Session = Depends(get_db),
):
    """
    이메일 인증 코드를 검증하는 엔드포인트
    """
    try:
        # Redis 연결 확인
        if not redis_client.ping():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redis 서버에 연결할 수 없습니다",
            )

        # Redis에서 저장된 인증 코드 조회
        redis_key = get_auth_key(email)
        stored_code = redis_client.get(redis_key)

        if not stored_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="인증 코드가 만료되었거나 인증을 요청하지 않은 이메일입니다.",
            )

        # stored_code가 bytes 타입인 경우에만 디코딩
        stored_code_str = (
            stored_code.decode("utf-8")
            if isinstance(stored_code, bytes)
            else stored_code
        )

        # 인증 코드 비교
        if auth_code != stored_code_str:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 인증 코드입니다"
            )

        # 인증 성공 시 Redis에서 코드 삭제
        redis_client.delete(redis_key)

        auth_user = models.AuthUserList(
            useremail=email
        )
        db.add(auth_user)
        db.commit()
        db.refresh(auth_user)

        return {
            "message": "이메일 인증이 완료되었습니다",
            "email": email,
            "verified": True,
        }

    except redis.exceptions.ConnectionError as e:
        logging.error(f"[!] VERIFICATION>> Redis connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis 서버에 연결할 수 없습니다",
        )
