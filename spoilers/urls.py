from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.CreateSpoiler.as_view()), # 신규 챌린지 스포일러 생성
    path("<int:pk>", views.SpoilerDetail.as_view()), # 개별 챌린지 스포일로 조회 및 수정
]