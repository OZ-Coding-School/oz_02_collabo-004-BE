from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
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

class ChallengeList(APIView): # 전체 챌린지 리스트 가져오기 (관리자, 로그인유저만 가능)
    #permission_classes=[IsOwnerOrStaff] #권한부여

    def get(self, request): 
        challenges = ChallengeInfo.objects.all()
        serializer = ChallengeInfoSerializer(challenges, many = True) 
        return Response(serializer.data)
    
class UpdateChallenge(APIView):  # 챌린지 정보 업데이트 하기 (관리자만 가능)
    #permission_classes=[IsStaff]

    def post(self, request, challengeinfo_id): 
        try:
            challenge_info = ChallengeInfo.objects.get(pk=challengeinfo_id)
        except ChallengeInfo.DoesNotExist:
            return Response({"message": "Challenge not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChallengeInfoSerializer(instance=challenge_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class  UserChallengeList(APIView): # 사용자가 신청한 챌린지 리스트 가져오기 (관리자, 결제유저만 가능)
    #permission_classes=[IsPaidUserOrStaff]

    def get(self, request, user_id):
        try:
            user_challenges = ChallengeInfo.objects.filter(user_id=user_id)
            serializer = ChallengeInfoSerializer(user_challenges, many=True)
            return Response(serializer.data)
        except ChallengeInfo.DoesNotExist:
            return Response({"error": "User challenges not found"}, status=status.HTTP_404_NOT_FOUND)

class UserChallengeDetail(APIView): # 신청한 챌린지 상세사항 보기(관리자, 결제유저만 가능) 
    #permission_classes=[IsPaidUserOrStaff] 
    def get(self, request, challengeinfo_id, user_id):
        try:
            challenge_info = ChallengeInfo.objects.get(pk=challengeinfo_id)
        except ChallengeInfo.DoesNotExist:
            return Response({"error": "Challenge not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 챌린지 정보에 연결된 책 정보 가져오기
        book_serializer = BookSerializer(challenge_info.book)

        # 모든 정보를 조합하여 응답 데이터 구성
        response_data = {
            "challenge_info" : ChallengeInfoSerializer(challenge_info).data,
            "book_info": book_serializer.data
        }

        return Response(response_data)