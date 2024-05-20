from django.shortcuts import render
from rest_framework import generics
from .serializers import SpoilerSerializer
from .models import Spoiler
from books.views import custom_handle_exception, IsStaffOrReadOnly

# 생성하기
class CreateSpoiler(generics.CreateAPIView):
    serializer_class = SpoilerSerializer
    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    handle_exception = custom_handle_exception


# 수정 및 불러오기
class SpoilerDetail(generics.RetrieveUpdateAPIView):

    serializer_class = SpoilerSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = Spoiler.objects.all()

    handle_exception = custom_handle_exception