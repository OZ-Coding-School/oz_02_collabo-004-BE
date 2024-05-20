# 기본 이미지 정의
FROM python:3.12

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드를 컨테이너의 작업 디렉토리로 복사
COPY . /app/

# 필요한 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Gunicorn 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bookspoiler.wsgi:application"]
