from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound

from .models import ChallengeInfo, ChallengeSpoiler, DoItComment
from .serializers import ChallengeInfoSerializer, ChallengeSpoilerSerializer, DoItCommentSerializer
from books.serializers import BookSerializer
from users.models import User
from books.models import Book
#from permissions import IsOwnerOrStaff, IsPaidUserOrStaff, IsStaff

# http method  정의    
class CreateChallenge(APIView):  # 신규챌린지 생성하기 (관리자만 가능)
    #permission_classes=[IsStaff]

    def post(self, request, book_id): 
        book = get_object_or_404(Book, pk=book_id)  # 주어진 book_id에 해당하는 Book 객체 가져오기
        request_data = request.data
        request_data['book'] = book.id

        serializer = ChallengeInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
