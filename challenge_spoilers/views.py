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


# 수정 및 불러오기
class ChallengeSpoilerDetail(generics.RetrieveUpdateAPIView):

    serializer_class = ChallengeSpoilerSerializer
    queryset = ChallengeSpoiler.objects.all()

    handle_exception = custom_handle_exception


# 챌린지별 챌린지 스포일러 불러오기
class ChallengeFiveSpoilers(generics.ListAPIView):

    serializer_class = ChallengeSpoilerSerializer

    def get_queryset(self):
        challenge_info_id = self.kwargs.get('challenge_info_id')
        
        five_spoilers = Review.objects.filter(challenge_info_id=challenge_info_id)

        return five_spoilers
