from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import DoItComment
from users.models import User
from challenges.models import ChallengeInfo
from challenge_spoilers.models import ChallengeSpoiler
from payment.models import Payment
from doitcomments.serializers import DoItCommentSerializer


# challenge용 스포일러 댓글관련
class CreateDIComment(APIView):  # 챌린지 스포일러에 댓글 생성하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def post(self, request, user_id, challengeinfo_id, challengespoiler_id):
        try:
            user = User.objects.get(pk=user_id)
            
            challenge_info = ChallengeInfo.objects.get(pk=challengeinfo_id)
            challengespoiler = ChallengeSpoiler.objects.get(pk=challengespoiler_id, challenge_info=challenge_info)

            user_payments = Payment.objects.filter(user_id=user_id)
            challenge_ids = [payment.challenge_info_id for payment in user_payments]

            if int(challengeinfo_id) not in challenge_ids:
                return Response({"error": "해당 챌린지는 결제되지 않았습니다."}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except ChallengeInfo.DoesNotExist:
            return Response({"error": "ChallengeInfo not found"}, status=status.HTTP_404_NOT_FOUND)
        except ChallengeSpoiler.DoesNotExist:
            return Response({"error": "ChallengeSpoiler not found"}, status=status.HTTP_404_NOT_FOUND)

        data_with_challengespoiler_id = request.data.copy()
        data_with_challengespoiler_id['challengespoiler_info'] = challengespoiler_id
        data_with_challengespoiler_id['user'] = user.id  

        serializer = DoItCommentSerializer(data=data_with_challengespoiler_id)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChallengeSpoilerComment(APIView): #챌린지 스포일러에 전체 댓글 가져오기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def get(self, request, challengespoiler_id):
        try:
            challengespoiler = ChallengeSpoiler.objects.get(pk=challengespoiler_id)
        except ChallengeSpoiler.DoesNotExist:
            return Response({"error": "ChallengeSpoiler not found"}, status=status.HTTP_404_NOT_FOUND)

        # challengespoiler_id에 연결된 DoItComment 댓글들을 가져옵니다.
        doit_comments = DoItComment.objects.filter(challengespoiler_info=challengespoiler)
        serializer = DoItCommentSerializer(doit_comments, many=True)
        return Response(serializer.data)
    
class UpdateDIComment(APIView): # 챌린지용 스포일러에 댓글 업데이트 하기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]

    def put(self, request, doitcomment_id): 
        try:
            doit_comment = DoItComment.objects.get(pk=doitcomment_id)
        except DoItComment.DoesNotExist:
            return Response({"message": "DoItComment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DoItCommentSerializer(doit_comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteDIComment(APIView): # 챌린지용 스포일러에 댓글 삭제학기 (관리자, 결제유저만 가능)
    #permission_classes = [IsPaidUserOrStaff]
    
    def post(self, request, doitcomment_id): 
        doitcomment_id = request.data.get('doitcomment_id')

        if not doitcomment_id:
            return Response({"error":"사용자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            doitcomment = DoItComment.objects.get(id=doitcomment_id)
        except DoItComment.DoesNotExist:
            return Response({"message": "DoItComment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        doitcomment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
