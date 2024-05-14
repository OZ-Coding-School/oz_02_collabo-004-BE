from django.shortcuts import render
from rest_framework import generics, status
from .serializers import ChallengeSpoilerSerializer
from .models import ChallengeSpoiler
from books.views import custom_handle_exception



# 생성하기
class CreateChallengeSpoiler(generics.CreateAPIView):
    serializer_class = ChallengeSpoilerSerializer

    def perform_create(self, serializer):
        serializer.save()

    handle_exception = custom_handle_exception