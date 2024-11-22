from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta
from sqlalchemy.orm import Session
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import base64

logging.basicConfig(level=logging.INFO)

# directory dependency
from SSSP.api.core.database import get_db
from SSSP.api.models import models
from datetime import datetime 
from zoneinfo import ZoneInfo
from SSSP.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.jwt.secret_key
ALGORITHM = settings.jwt.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.jwt.token_expire_minutes)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + expires_delta
    else:
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_by_jwt(token, db: Session = Depends(get_db)):
    username = verify_token(token)
    user = db.query(models.User).filter(models.User.username == username).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot find user id"
        )
    
    return user
    
    

def verify_token(token: str):
    try:
        logging.debug(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        logging.info(f"[*] AUTH>> Decoded payload: {payload}")
        logging.info(f"[*] AUTH>> sub from payload: {username}")
        return username
    except JWTError as e:
        logging.debug(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to verify JWT token.",
        )

def generate_auth_code(length: int = 6) -> str:
    """숫자로 된 인증 코드 생성"""
    return "".join(random.choices(string.digits, k=length))


def get_image_base64(image_path: str) -> str:
    """이미지를 base64로 인코딩"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


async def send_auth_email(to: str, auth_code: str):
    try:
        favicon_base64 = get_image_base64(settings.favicon_path)
        subject = "SSSP 이메일 인증"

        html_content = f"""
        <html>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f7f9; border: 1px solid #e0e0e0; border-radius: 8px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <img src="data:image/ico;base64,{favicon_base64}" style="width: 80px; height: auto; margin-bottom: 15px;" alt="SSSP Logo">
                        <h1 style="font-size: 24px; font-weight: bold; color: #006e93; margin: 0;">SSSP 이메일 인증</h1>
                        <p style="font-size: 14px; color: #62c6c4;">회원가입을 위한 인증 코드입니다.</p>
                    </div>
                    <div style="font-size: 16px; color: #333; line-height: 1.6; margin-bottom: 20px;">
                        <p>안녕하세요,</p>
                        <p>
                            SSSP를 이용해 주셔서 감사합니다. 아래 인증번호를 입력하여 
                            <span style="color: #62c6c4; font-weight: bold;">이메일 인증</span>을 완료해주세요.
                        </p>
                    </div>
                    <div style="background-color: #f1f3f7; padding: 15px; text-align: center; font-size: 28px; font-weight: bold; letter-spacing: 5px; margin: 20px 0; color: #02a6cb; border: 1px dashed #62c6c4; border-radius: 8px;">
                        {auth_code}
                    </div>
                    <div style="font-size: 16px; color: #333; line-height: 1.6; margin-bottom: 20px;">
                        <p>인증번호는 <span style="color: #62c6c4; font-weight: bold;">5분</span> 동안만 유효합니다.</p>
                    </div>
                    <div style="margin-top: 30px; font-size: 12px; color: #666; text-align: center; line-height: 1.4;">
                        <p style="margin: 5px 0;">본 메일은 발신 전용입니다.</p>
                        <p style="margin: 5px 0;">&copy; 2024 SSSP. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """

        # 이메일 메시지 생성
        message = MIMEMultipart("alternative")
        message["From"] = settings.email.sender_email
        message["To"] = to
        message["Subject"] = subject
        message["MIME-Version"] = "1.0"

        # HTML만 포함하되, Content-Type 헤더를 명확하게 설정
        html_part = MIMEText(html_content, "html", "utf-8")
        html_part["Content-Type"] = "text/html; charset=utf-8"

        message.attach(html_part)

        # Gmail SMTP 설정에 Content-Transfer-Encoding 추가
        message["Content-Transfer-Encoding"] = "8bit"

        # SMTP 서버 연결 및 이메일 전송
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.email.sender_email, settings.email.sender_password)
            server.send_message(message)

        logging.info(f"[*] EMAIL>> Successfully sent auth email to {to}")
        return True

    except Exception as e:
        logging.error(f"[!] EMAIL>> Failed to send auth email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send auth email",
        )
