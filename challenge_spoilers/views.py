from django.shortcuts import render
from rest_framework import generics
from .serializers import ChallengeSpoilerSerializer
from .models import ChallengeSpoiler
from books.views import custom_handle_exception, IsStaffOrReadOnly



# 생성하기
class CreateChallengeSpoiler(generics.CreateAPIView):
    serializer_class = ChallengeSpoilerSerializer
    permission_classes = [IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    handle_exception = custom_handle_exception


# 수정 및 불러오기
class ChallengeSpoilerDetail(generics.RetrieveUpdateAPIView):

    serializer_class = ChallengeSpoilerSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = ChallengeSpoiler.objects.all()

    handle_exception = custom_handle_exception


# 챌린지별 챌린지 스포일러 불러오기
class ChallengeFiveSpoilers(generics.ListAPIView):

    serializer_class = ChallengeSpoilerSerializer

    def get_queryset(self):
        challenge_info_id = self.kwargs.get('challenge_info_id')
        
        five_spoilers = ChallengeSpoiler.objects.filter(challenge_info_id=challenge_info_id)

        return five_spoilers

    handle_exception = custom_handle_exception

# 책별 챌린지 스포일러 불러오기
class BookFiveSpoilers(generics.ListAPIView):

    serializer_class = ChallengeSpoilerSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        
        five_spoilers = ChallengeSpoiler.objects.filter(book_id=book_id)

        return five_spoilers



