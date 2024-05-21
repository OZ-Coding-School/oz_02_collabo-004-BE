from django.shortcuts import render
from rest_framework import generics
from .serializers import ReviewSerializer
from .models import Review
from books.views import custom_handle_exception, IsStaffOrReadOnly
from django.shortcuts import get_object_or_404
from books.models import Book

# 생성하기
class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    #permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    handle_exception = custom_handle_exception

# 수정 및 불러오기
class ReviewDetail(generics.RetrieveUpdateAPIView):

    serializer_class = ReviewSerializer
    #permission_classes = [IsStaffOrReadOnly]
    queryset = Review.objects.all()

    handle_exception = custom_handle_exception


# 책 별 추천 서평 조회
class BookReviews(generics.ListAPIView):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        
        reviews = Review.objects.filter(book_id=book_id)

        return reviews

    handle_exception = custom_handle_exception