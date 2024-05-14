from django.urls import path
from . import views

'''
/keywords
/keyword/create
/keyword/update/{keyword_id} 
'''

urlpatterns = [
    # path("", views.KeywordList.as_view()), # 키워드 전체 조회
    path("create/", views.CreateKeyword.as_view()), # 신규 키워드 생성
    path("<int:pk>", views.KeywordDetail.as_view()), # 개별 키워드 조회 및 수정
]