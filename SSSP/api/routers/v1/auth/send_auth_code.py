from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from typing import List
import logging
from redis import Redis
import redis

from SSSP.api.core.auth import generate_auth_code, send_auth_email
from SSSP.api.core.redis import (
    get_redis,
    get_auth_key,
    AUTH_CODE_EXPIRE_MINUTES,
)

router = APIRouter()


@router.post("/send-auth-code")
async def send_auth_code(
    receiver_email: str,
    background_tasks: BackgroundTasks,
    redis_client: Redis = Depends(get_redis),
):
    """
    이메일 인증 코드를 생성하고 전송하는 엔드포인트
    """
    try:
        # Redis 연결 확인
        if not redis_client.ping():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redis 서버에 연결할 수 없습니다",
            )

        # 기존 인증 코드 확인
        redis_key = get_auth_key(receiver_email)
        existing_code = redis_client.get(redis_key)

        if existing_code:
            # 기존 인증 코드가 있다면 삭제
            redis_client.delete(redis_key)
            logging.info(
                f"[*] AUTH CODE>> Deleted existing auth code for {receiver_email}"
            )

        # 인증 코드 생성
        auth_code = generate_auth_code()

        # Redis에 인증 코드 저장 (5분 유효)
        redis_client.set(
            redis_key,
            auth_code.encode(),  # 문자열을 바이트로 인코딩
            ex=AUTH_CODE_EXPIRE_MINUTES * 60,  # seconds로 변환
        )

        # 이메일 전송을 백그라운드 태스크로 변경
        background_tasks.add_task(send_auth_email, receiver_email, auth_code)

        return {
            "receiver_email": receiver_email,
            "expires_in": f"{AUTH_CODE_EXPIRE_MINUTES}분",
        }

    except redis.exceptions.ConnectionError as e:
        logging.error(f"[!] AUTH CODE>> Redis connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis 서버에 연결할 수 없습니다",
        )
    except Exception as e:
        logging.error(f"[!] AUTH CODE>> Failed to send auth code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="인증 코드 전송에 실패했습니다",
        )
