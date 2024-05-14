### 가상환경 설정 후 활성화(윈도우 기준)
```
python -m venv .venv
```
```
.venv/scripts/activate
```
### requirements.txt 작성 후 패키지 설치
```
pip install -r requirements.txt
```
### pip 업그레이드 하라고 귀찮게 하니 해버리자
```
python -m pip install --upgrade pip
```
### 프로젝트 시작 (설정부분 생성)
```
django-admin startproject bookspoiler .
```
### 첫번째 마이그레이트
```
python manage.py migrate
```
### 메인 생성 후 settings.py에 연결. 언어랑 시간대도 바꾸자.
```
python manage.py startapp users
```
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
]
```
### settings.py 에서 해당부분을 찾아 바꾸면 된다.
```
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'
```
### kakao allauth 관련 설정을 settings.py, urls,py에 넣었으나 작동오류 발생
```
마이그레이트까지 성공했으나 localhost:8000 했을 경우 404가 뜬다.
/admin은 500 에러가 뜬다. 템플릿이 없어서 그런건가 추측만 하고 있다.
→ /admin의 경우 settings.py에서 'django.contrib.sites'의 문제여서 주석처리함.
```
### localhost:8000/users 호출 성공 (May 6th. 2024.)
```
카카오 로그인과 연결이 되었는지는 모르겠음.
그러나 Django 기본 제공인 api 화면으로 보여진다고 생각함.
시리얼라이저 부분을 포함하여 계속 검토하며 수정 작업 나갈 예정
```