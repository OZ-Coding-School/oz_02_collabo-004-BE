from django.urls import path
from .views import CreateDIComment, ChallengeSpoilerComment, UpdateDIComment, DeleteDIComment

urlpatterns = [

# 챌린지 스포일러 댓글 생성, 가져오기, 수정, 삭제
    path("dicomment/create/<int:user_id>/<int:challengeinfo_id>/<int:challengespoiler_id>",CreateDIComment.as_view(), name="create_dicomment"),
    path("dicomments/<int:challengespoiler_id>", ChallengeSpoilerComment.as_view(), name="dicomments_list"),
    path("dicomment/update/<int:doitcomment_id>", UpdateDIComment.as_view(), name="update_dicomment"),
    path("dicomment/delete/<int:doitcomment_id>", DeleteDIComment.as_view(), name="delete_dicomment"),

]