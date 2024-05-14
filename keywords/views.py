from django.shortcuts import render
from .serializers import KeywordSerializer
from rest_framework import generics
from rest_framework.exceptions import NotFound
from .models import Keyword
from books.views import custom_handle_exception

# 전체 키워드 목록 조회
class KeywordList(generics.ListAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    handle_exception = custom_handle_exception


# 생성하기
class CreateKeyword(generics.CreateAPIView):
    serializer_class = KeywordSerializer

    def perform_create(self, serializer):
        serializer.save()

    handle_exception = custom_handle_exception
    


# 개별 수정 및 불러오기
class KeywordDetail(generics.RetrieveUpdateAPIView):

    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all()

    handle_exception = custom_handle_exception


# 책 별 키워드 조회
class BookKeywords(generics.ListAPIView):
    
    serializer_class = KeywordSerializer

    def get_queryset(self):

        book_id = self.kwargs.get('book_id')

        keywords = Keyword.objects.filter(book_id=book_id)
        
        return keywords
