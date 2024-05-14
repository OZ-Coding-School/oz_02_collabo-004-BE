from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from rest_framework import status
from rest_framework.exceptions import (ValidationError, NotFound, APIException)
from rest_framework.pagination import PageNumberPagination



def custom_handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({"detail": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotFound):
            return Response({"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, ValidationError) and exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            return Response({"detail": "Unprocessable Entity."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif isinstance(exc, APIException):
            return Response({"detail": "Server Internal Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return super().handle_exception(exc)


# 등록완료 상태인 도서 리스트 불러오기
class Books(generics.ListAPIView):
    queryset = Book.objects.filter(is_exposed=True)
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    handle_exception = custom_handle_exception


# 전체 도서 리스트 불러오기
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination
    # permission_classes = [IsStaffOrReadOnly]

    handle_exception = custom_handle_exception

# 개별 도서 리스트 관리 및 개별 도서 정보 수정하기
class BookDetail(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsStaffOrReadOnly]

    handle_exception = custom_handle_exception

