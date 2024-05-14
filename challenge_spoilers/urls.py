from django.urls import path
from . import views


urlpatterns = [
    path("spoiler/<int:pk>/", views.ChallengeSpoilerDetail.as_view()), # 개별 챌린지 스포일러 조회, 수정
    path("for_challenge_spoiler/create/", views.CreateChallengeSpoiler.as_view()),
]