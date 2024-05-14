from django.urls import path
from . import views
'''
urlpatterns = [
    path("", views.Books.as_view()), # 등록완료 상태인 도서 리스트 불러오기
    path("all/", views.BookList.as_view()), # 전체 도서 리스트 불러오기
    path("book/create/", views.BookCreate.as_view()), # 신규 도서 생성하기
    path("book/<int:pk>/", views.BookDetail.as_view()), # 개별 도서 리스트 관리 및 개별 도서 정보 수정하기
]
'''