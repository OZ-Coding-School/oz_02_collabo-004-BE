from django.shortcuts import render
from rest_framework import generics
from .serializers import SpoilerSerializer
from .models import Spoiler
from books.views import custom_handle_exception

# 생성하기
class CreateSpoiler(generics.CreateAPIView):
    serializer_class = SpoilerSerializer

    def perform_create(self, serializer):
        serializer.save()

    handle_exception = custom_handle_exception


# 수정 및 불러오기
class SpoilerDetail(generics.RetrieveUpdateAPIView):

    serializer_class = SpoilerSerializer
    queryset = Spoiler.objects.all()

    handle_exception = custom_handle_exception