from django.urls import path
from .views import CreateChallenge, ChallengeList

urlpatterns = [
    # 챌린지 생성하기 # 전체 챌린지 리스트 가져오기 # 챌린지 정보 업데이트 하기  
    path("challenge/create/<int:book_id>",CreateChallenge.as_view(), name='create_challenge'),
    path("challenges/", ChallengeList.as_view(), name='challenge_list'),
]