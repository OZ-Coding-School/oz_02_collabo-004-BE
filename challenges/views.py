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
    
class UserChallengeDo(APIView):  # 챌린지 참여현황 가져오기 - 몇 % 진행됬는지 - 구현 순서 중

    def get(self, request, user_id):
        # 해당 사용자가 신청한 모든 챌린지 가져오기
        user_challenges = ChallengeInfo.objects.filter(user_id=user_id)
        user_doing = []

        for challenge_info in user_challenges:
            total_days = 5  # 도전 챌린지 총 day 수
            challenge_spoilers = ChallengeSpoiler.objects.filter(challenge_info=challenge_info)
            completed_days = 0

            for day in range(1, total_days + 1):
                # 해당 챌린지의 특정 일차별 스포일러 가져오기
                try:
                    spoiler = challenge_spoilers.get(day=str(day))
                except ChallengeSpoiler.DoesNotExist:
                    continue
                
                # 해당 일차별 스포일러에 달린 사용자의 댓글 수 계산
                comment_days = DoItComment.objects.filter(challengespoiler_info=spoiler, user_id=user_id).count()
                if comment_days > 0:
                    completed_days += 1

            # 챌린지의 완료 일수를 기반으로 사용자의 수행 백분율 계산
            doing_percentage = (completed_days / total_days) * 100
            user_doing.append({
                'user_id': user_id,
                'challengeinfo_id': challenge_info.id,
                'user_doing': int(doing_percentage)  # 소수점 이하 버림
            })

        return Response(user_doing)
    

# challenge용 스포일러 댓글관련
class CreateDIComment(APIView):  #챌린지 스포일러에 댓글 생성하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def post(self, request, challengespoiler_id):
        try:
            challengespoiler = ChallengeSpoiler.objects.get(pk=challengespoiler_id)
        except ChallengeSpoiler.DoesNotExist:
            return Response({"error": "ChallengeSpoiler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 요청 데이터에 spoiler_id와 user 정보 추가하여 DoItCommentSerializer 생성
        data_with_challengespoiler_id = request.data.copy()
        data_with_challengespoiler_id['challengespoiler_info'] = challengespoiler_id
        data_with_challengespoiler_id['user'] = request.user.id  # 현재 사용자 정보를 추가
        
        serializer = DoItCommentSerializer(data=data_with_challengespoiler_id)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)