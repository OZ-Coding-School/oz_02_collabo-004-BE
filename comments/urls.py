from django.urls import path
from .views import CreateComment, SpoilerComment

# 일반 스포일러 댓글 생성, 가져오기, 수정, 삭제
urlpatterns = [
    path("comment/create/<int:spoiler_id>",CreateComment.as_view(), name="create_comment"),
    path("comments/<int:spoiler_id>", SpoilerComment.as_view(), name="comments_list"),
]