from django.urls import path
from . import views


urlpatterns = [
    path("<int:pk>/", views.ChallengeSpoilerDetail.as_view()), # 개별 챌린지 스포일러 조회, 수정
    path("create/", views.CreateChallengeSpoiler.as_view()), # 챌린지 스포일러 생성
    path("list/", views.BookFiveSpoilers.as_view()), # 책별 챌린지 스포일러 조회
]