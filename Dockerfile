# Cloud Run에서 안정적인 버전 권장 (3.11)
FROM python:3.11-slim

# 로그 버퍼링 방지 + pyc 생성 방지
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 의존성 먼저 복사/설치 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# Cloud Run은 PORT 환경변수를 줍니다.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
