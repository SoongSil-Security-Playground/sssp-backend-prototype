# python:3.9-slim 사용 (필요 시 버전 변경)
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일을 복사
COPY . .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI가 사용할 포트 설정
EXPOSE 443

# FastAPI 앱 실행
CMD ["uvicorn", "SSSP.api.app:apimain", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/etc/letsencrypt/live/sssp.live/privkey.pem", "--ssl-certfile", "/etc/letsencrypt/live/sssp.live/fullchain.pem"]
#CMD ["uvicorn", "SSSP.api.app:apimain", "--host", "0.0.0.0", "--port", "443"]

