from django.urls import path
from .views import CreateComment

# 일반 스포일러 댓글 생성, 가져오기, 수정, 삭제
urlpatterns = [
    path("comment/create/<int:spoiler_id>",CreateComment.as_view(), name="create_comment"),
]