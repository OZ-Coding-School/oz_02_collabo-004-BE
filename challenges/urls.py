from django.urls import path
from .views import CreateChallenge

urlpatterns = [
    # 챌린지 생성하기 # 챌린지 정보 업데이트 하기, # 전체 챌린지 리스트 가져오기,  
    path("challenge/create/<int:book_id>",CreateChallenge.as_view(), name='create_challenge'),
]