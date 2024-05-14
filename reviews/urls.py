from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.CreateReview.as_view()), # 신규 추천서평 생성
    path("<int:pk>/", views.ReviewDetail.as_view()), # 개별 추천서평 조회 및 수정
]